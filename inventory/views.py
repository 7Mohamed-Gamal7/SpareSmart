from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, F
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from accounts.views import permission_required
from .models import Product, Category, Brand, Customer, Supplier, StockMovement, InventoryAlert
from .forms import (
    ProductForm, CategoryForm, BrandForm, CustomerForm, SupplierForm,
    StockAdjustmentForm, ProductFilterForm, BulkActionForm
)
from dashboard.models import ActivityLog
import json
from datetime import datetime, timedelta
from django.utils import timezone

@login_required
@permission_required('view_products')
def product_list(request):
    """List all products with filtering and pagination"""
    products = Product.objects.select_related('category', 'brand').all()
    filter_form = ProductFilterForm(request.GET)
    
    # Apply filters
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        category = filter_form.cleaned_data.get('category')
        brand = filter_form.cleaned_data.get('brand')
        vehicle_type = filter_form.cleaned_data.get('vehicle_type')
        stock_status = filter_form.cleaned_data.get('stock_status')
        is_active = filter_form.cleaned_data.get('is_active')
        
        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(sku__icontains=search) |
                Q(barcode__icontains=search) |
                Q(part_number__icontains=search) |
                Q(oem_number__icontains=search)
            )
        
        if category:
            products = products.filter(category=category)
        
        if brand:
            products = products.filter(brand=brand)
        
        if vehicle_type:
            products = products.filter(category__vehicle_type=vehicle_type)
        
        if stock_status:
            if stock_status == 'out_of_stock':
                products = products.filter(current_stock=0)
            elif stock_status == 'low_stock':
                products = products.filter(
                    current_stock__gt=0,
                    current_stock__lte=F('reorder_level')
                )
            elif stock_status == 'in_stock':
                products = products.filter(current_stock__gt=F('reorder_level'))
        
        if is_active:
            products = products.filter(is_active=bool(int(is_active)))
    
    # Pagination
    paginator = Paginator(products, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate totals
    total_products = products.count()
    total_value = products.aggregate(
        total=Sum(F('current_stock') * F('cost_price'))
    )['total'] or 0
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'total_products': total_products,
        'total_value': total_value,
    }
    
    return render(request, 'inventory/product_list.html', context)

@login_required
@permission_required('add_products')
def product_create(request):
    """Create new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save()
                
                # Log activity
                ActivityLog.objects.create(
                    user=request.user,
                    action='create',
                    description=f'Created product: {product.name} ({product.sku})',
                    content_object=product
                )
                
                # Create initial stock movement if current_stock > 0
                if product.current_stock > 0:
                    StockMovement.objects.create(
                        product=product,
                        movement_type='adjustment',
                        quantity=product.current_stock,
                        unit_cost=product.cost_price,
                        reference_number='INITIAL',
                        notes='Initial stock entry',
                        created_by=request.user
                    )
                
                messages.success(request, f'Product "{product.name}" created successfully.')
                return redirect('inventory:product_detail', product_id=product.id)
                
            except Exception as e:
                messages.error(request, f'Error creating product: {str(e)}')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add New Product',
        'action': 'Create'
    }
    
    return render(request, 'inventory/product_form.html', context)

@login_required
@permission_required('view_products')
def product_detail(request, product_id):
    """View product details"""
    product = get_object_or_404(Product, id=product_id)
    
    # Get recent stock movements
    recent_movements = product.stock_movements.select_related('created_by').order_by('-created_at')[:10]
    
    # Calculate profit margin
    profit_margin = 0
    if product.cost_price > 0:
        profit_margin = ((product.selling_price - product.cost_price) / product.cost_price) * 100
    
    context = {
        'product': product,
        'recent_movements': recent_movements,
        'profit_margin': profit_margin,
        'total_value': product.current_stock * product.cost_price,
    }
    
    return render(request, 'inventory/product_detail.html', context)

@login_required
@permission_required('edit_products')
def product_update(request, product_id):
    """Update product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                old_stock = product.current_stock
                updated_product = form.save()
                
                # Log activity
                ActivityLog.objects.create(
                    user=request.user,
                    action='update',
                    description=f'Updated product: {updated_product.name} ({updated_product.sku})',
                    content_object=updated_product
                )
                
                # If stock changed, create stock movement
                if old_stock != updated_product.current_stock:
                    movement_type = 'adjustment'
                    quantity = abs(updated_product.current_stock - old_stock)
                    if updated_product.current_stock > old_stock:
                        # Stock increase
                        pass
                    else:
                        # Stock decrease
                        quantity = -quantity
                    
                    StockMovement.objects.create(
                        product=updated_product,
                        movement_type=movement_type,
                        quantity=quantity,
                        unit_cost=updated_product.cost_price,
                        reference_number='ADJUSTMENT',
                        notes='Stock adjusted via product update',
                        created_by=request.user
                    )
                
                messages.success(request, f'Product "{updated_product.name}" updated successfully.')
                return redirect('inventory:product_detail', product_id=updated_product.id)
                
            except Exception as e:
                messages.error(request, f'Error updating product: {str(e)}')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': f'Edit Product: {product.name}',
        'action': 'Update'
    }
    
    return render(request, 'inventory/product_form.html', context)

@login_required
@permission_required('manage_categories')
def category_list(request):
    """List all categories with filtering and statistics"""
    categories = Category.objects.prefetch_related('products').all()
    
    # Apply filters
    search = request.GET.get('search')
    vehicle_type = request.GET.get('vehicle_type')
    sort = request.GET.get('sort', 'name')
    
    if search:
        categories = categories.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    if vehicle_type:
        categories = categories.filter(vehicle_type=vehicle_type)
    
    # Sorting
    if sort == 'name':
        categories = categories.order_by('name')
    elif sort == 'vehicle_type':
        categories = categories.order_by('vehicle_type', 'name')
    elif sort == 'product_count':
        categories = categories.annotate(product_count=Count('products')).order_by('-product_count')
    elif sort == 'created_at':
        categories = categories.order_by('-created_at')
    
    # Annotate with product count
    categories = categories.annotate(product_count=Count('products'))
    
    # Pagination
    paginator = Paginator(categories, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_categories = Category.objects.count()
    motorcycle_categories = Category.objects.filter(vehicle_type='motorcycle').count()
    car_categories = Category.objects.filter(vehicle_type='car').count()
    tuktuk_categories = Category.objects.filter(vehicle_type='tuktuk').count()
    
    context = {
        'categories': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_categories': total_categories,
        'motorcycle_categories': motorcycle_categories,
        'car_categories': car_categories,
        'tuktuk_categories': tuktuk_categories,
    }
    
    return render(request, 'inventory/category_list.html', context)

@login_required
@permission_required('manage_categories')
def category_create(request):
    """Create new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            
            ActivityLog.objects.create(
                user=request.user,
                action='create',
                description=f'Created category: {category.name}',
                content_object=category
            )
            
            messages.success(request, f'Category "{category.name}" created successfully.')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Add New Category'
    }
    
    return render(request, 'inventory/category_form.html', context)

@login_required
@permission_required('view_products')
def customer_list(request):
    """List all customers with comprehensive filtering and statistics"""
    customers = Customer.objects.all()
    
    # Apply filters
    search = request.GET.get('search')
    customer_type = request.GET.get('customer_type')
    status = request.GET.get('status')
    balance_filter = request.GET.get('balance_filter')
    sort = request.GET.get('sort', 'name')
    
    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(company_name__icontains=search)
        )
    
    if customer_type:
        customers = customers.filter(customer_type=customer_type)
    
    if status:
        if status == 'active':
            customers = customers.filter(is_active=True)
        elif status == 'inactive':
            customers = customers.filter(is_active=False)
    
    if balance_filter:
        if balance_filter == 'positive':
            customers = customers.filter(balance__gt=0)
        elif balance_filter == 'negative':
            customers = customers.filter(balance__lt=0)
        elif balance_filter == 'zero':
            customers = customers.filter(balance=0)
    
    # Sorting
    if sort == 'name':
        customers = customers.order_by('name')
    elif sort == 'created_at':
        customers = customers.order_by('-created_at')
    elif sort == 'balance':
        customers = customers.order_by('-balance')
    elif sort == 'last_sale':
        customers = customers.order_by('-last_sale_date')
    
    # Pagination
    paginator = Paginator(customers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    total_credit_balance = Customer.objects.filter(balance__gt=0).aggregate(
        total=Sum('balance'))['total'] or 0
    total_debit_balance = abs(Customer.objects.filter(balance__lt=0).aggregate(
        total=Sum('balance'))['total'] or 0)
    
    context = {
        'customers': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_customers': total_customers,
        'active_customers': active_customers,
        'total_credit_balance': total_credit_balance,
        'total_debit_balance': total_debit_balance,
    }
    
    return render(request, 'inventory/customer_list.html', context)

@login_required
@permission_required('add_products')
def customer_create(request):
    """Create new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            
            ActivityLog.objects.create(
                user=request.user,
                action='create',
                description=f'Created customer: {customer.name}',
                content_object=customer
            )
            
            messages.success(request, f'Customer "{customer.name}" created successfully.')
            return redirect('inventory:customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm()
    
    context = {
        'form': form,
        'title': 'Add New Customer'
    }
    
    return render(request, 'inventory/customer_form.html', context)

@login_required
@permission_required('view_products')
def customer_detail(request, customer_id):
    """View customer details"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    # Get recent sales (will implement when sales module is ready)
    # recent_sales = customer.sales.order_by('-sale_date')[:10]
    
    context = {
        'customer': customer,
        # 'recent_sales': recent_sales,
    }
    
    return render(request, 'inventory/customer_detail.html', context)

@login_required
@permission_required('view_products')
def supplier_list(request):
    """List all suppliers with comprehensive filtering and statistics"""
    suppliers = Supplier.objects.all()
    
    # Apply filters
    search = request.GET.get('search')
    status = request.GET.get('status')
    rating = request.GET.get('rating')
    balance_filter = request.GET.get('balance_filter')
    sort = request.GET.get('sort', 'name')
    
    if search:
        suppliers = suppliers.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(company_name__icontains=search)
        )
    
    if status:
        if status == 'active':
            suppliers = suppliers.filter(is_active=True)
        elif status == 'inactive':
            suppliers = suppliers.filter(is_active=False)
    
    if rating:
        suppliers = suppliers.filter(rating__gte=int(rating))
    
    if balance_filter:
        if balance_filter == 'positive':
            suppliers = suppliers.filter(balance__gt=0)
        elif balance_filter == 'negative':
            suppliers = suppliers.filter(balance__lt=0)
        elif balance_filter == 'zero':
            suppliers = suppliers.filter(balance=0)
    
    # Sorting
    if sort == 'name':
        suppliers = suppliers.order_by('name')
    elif sort == 'created_at':
        suppliers = suppliers.order_by('-created_at')
    elif sort == 'balance':
        suppliers = suppliers.order_by('-balance')
    elif sort == 'rating':
        suppliers = suppliers.order_by('-rating')
    
    # Pagination
    paginator = Paginator(suppliers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    total_suppliers = Supplier.objects.count()
    active_suppliers = Supplier.objects.filter(is_active=True).count()
    total_payable = Supplier.objects.filter(balance__gt=0).aggregate(
        total=Sum('balance'))['total'] or 0
    
    # This will be properly calculated when purchase module is implemented
    total_purchases_this_month = 0
    
    context = {
        'suppliers': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_suppliers': total_suppliers,
        'active_suppliers': active_suppliers,
        'total_payable': total_payable,
        'total_purchases_this_month': total_purchases_this_month,
    }
    
    return render(request, 'inventory/supplier_list.html', context)

@login_required
@permission_required('add_products')
def supplier_create(request):
    """Create new supplier"""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            
            ActivityLog.objects.create(
                user=request.user,
                action='create',
                description=f'Created supplier: {supplier.name}',
                content_object=supplier
            )
            
            messages.success(request, f'Supplier "{supplier.name}" created successfully.')
            return redirect('inventory:supplier_detail', supplier_id=supplier.id)
    else:
        form = SupplierForm()
    
    context = {
        'form': form,
        'title': 'Add New Supplier'
    }
    
    return render(request, 'inventory/supplier_form.html', context)

@login_required
@permission_required('view_products')
def supplier_detail(request, supplier_id):
    """View supplier details"""
    supplier = get_object_or_404(Supplier, id=supplier_id)
    
    # Get recent purchases (will implement when purchases module is ready)
    # recent_purchases = supplier.purchases.order_by('-order_date')[:10]
    
    context = {
        'supplier': supplier,
        # 'recent_purchases': recent_purchases,
    }
    
    return render(request, 'inventory/supplier_detail.html', context)

@login_required
@permission_required('view_stock_reports')
def stock_movements(request):
    """View stock movements"""
    movements = StockMovement.objects.select_related('product', 'created_by').order_by('-created_at')
    
    # Filtering
    product_id = request.GET.get('product')
    movement_type = request.GET.get('movement_type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if product_id:
        movements = movements.filter(product_id=product_id)
    
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    
    if date_from:
        movements = movements.filter(created_at__date__gte=date_from)
    
    if date_to:
        movements = movements.filter(created_at__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(movements, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'movement_types': StockMovement.MOVEMENT_TYPE_CHOICES,
        'products': Product.objects.filter(is_active=True).order_by('name'),
        'filters': {
            'product': product_id,
            'movement_type': movement_type,
            'date_from': date_from,
            'date_to': date_to,
        }
    }
    
    return render(request, 'inventory/stock_movements.html', context)

@login_required
@permission_required('view_stock_reports')
def inventory_alerts(request):
    """View inventory alerts"""
    alerts = InventoryAlert.objects.select_related('product').filter(status='active').order_by('-created_at')
    
    context = {
        'alerts': alerts,
    }
    
    return render(request, 'inventory/alerts.html', context)

@login_required
@permission_required('view_stock_reports')
def low_stock_report(request):
    """Generate low stock report"""
    low_stock_products = Product.objects.filter(
        current_stock__lte=F('reorder_level'),
        is_active=True
    ).select_related('category', 'brand').order_by('current_stock')
    
    out_of_stock_products = Product.objects.filter(
        current_stock=0,
        is_active=True
    ).select_related('category', 'brand').order_by('name')
    
    context = {
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'total_low_stock': low_stock_products.count(),
        'total_out_of_stock': out_of_stock_products.count(),
    }
    
    return render(request, 'inventory/low_stock_report.html', context)

@login_required
@permission_required('edit_products')
@require_http_methods(["POST"])
def bulk_action(request):
    """Handle bulk actions on products"""
    form = BulkActionForm(request.POST)
    
    if form.is_valid():
        action = form.cleaned_data['action']
        selected_products = form.cleaned_data['selected_products']
        
        try:
            product_ids = [int(pid) for pid in selected_products.split(',')]
            products = Product.objects.filter(id__in=product_ids)
            
            if action == 'activate':
                products.update(is_active=True)
                message = f'{products.count()} products activated successfully.'
            elif action == 'deactivate':
                products.update(is_active=False)
                message = f'{products.count()} products deactivated successfully.'
            elif action == 'delete':
                count = products.count()
                products.delete()
                message = f'{count} products deleted successfully.'
            elif action == 'update_category':
                new_category = form.cleaned_data.get('new_category')
                if new_category:
                    products.update(category=new_category)
                    message = f'{products.count()} products updated with new category.'
                else:
                    message = 'Please select a category.'
            elif action == 'update_brand':
                new_brand = form.cleaned_data.get('new_brand')
                if new_brand:
                    products.update(brand=new_brand)
                    message = f'{products.count()} products updated with new brand.'
                else:
                    message = 'Please select a brand.'
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action='update',
                description=f'Bulk action: {action} on {len(product_ids)} products'
            )
            
            messages.success(request, message)
            
        except Exception as e:
            messages.error(request, f'Error performing bulk action: {str(e)}')
    else:
        messages.error(request, 'Invalid bulk action request.')
    
    return redirect('inventory:product_list')

# Enhanced Inventory Alerts Management

@login_required
@permission_required('view_stock_reports')
def alerts_dashboard(request):
    """Enhanced inventory alerts dashboard"""
    # Get active alerts grouped by type
    alerts = InventoryAlert.objects.select_related('product__category', 'product__brand').filter(status='active')
    
    # Count by alert type
    alert_counts = {
        'out_of_stock': alerts.filter(alert_type='out_of_stock').count(),
        'low_stock': alerts.filter(alert_type='low_stock').count(),
        'reorder': alerts.filter(alert_type='reorder').count(),
        'overstock': alerts.filter(alert_type='overstock').count(),
    }
    
    # Get recent alerts
    recent_alerts = alerts.order_by('-created_at')[:20]
    
    # Get critical alerts (out of stock and low stock)
    critical_alerts = alerts.filter(alert_type__in=['out_of_stock', 'low_stock']).order_by('-created_at')
    
    # Calculate total value of affected inventory
    affected_value = 0
    for alert in alerts:
        affected_value += alert.product.current_stock * alert.product.cost_price
    
    context = {
        'alert_counts': alert_counts,
        'recent_alerts': recent_alerts,
        'critical_alerts': critical_alerts,
        'total_alerts': sum(alert_counts.values()),
        'affected_value': affected_value,
    }
    
    return render(request, 'inventory/alerts_dashboard.html', context)

@login_required
@permission_required('view_stock_reports')
def alerts_list(request):
    """List all inventory alerts with filtering"""
    alerts = InventoryAlert.objects.select_related('product__category', 'product__brand', 'acknowledged_by')
    
    # Filtering
    alert_type = request.GET.get('alert_type')
    status = request.GET.get('status', 'active')
    search = request.GET.get('search')
    vehicle_type = request.GET.get('vehicle_type')
    
    if alert_type:
        alerts = alerts.filter(alert_type=alert_type)
    
    if status:
        alerts = alerts.filter(status=status)
    
    if search:
        alerts = alerts.filter(
            Q(product__name__icontains=search) |
            Q(product__sku__icontains=search) |
            Q(message__icontains=search)
        )
    
    if vehicle_type:
        alerts = alerts.filter(product__category__vehicle_type=vehicle_type)
    
    alerts = alerts.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(alerts, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'alert_types': InventoryAlert.ALERT_TYPE_CHOICES,
        'status_choices': InventoryAlert.STATUS_CHOICES,
        'vehicle_types': Category.VEHICLE_TYPE_CHOICES,
        'filters': {
            'alert_type': alert_type,
            'status': status,
            'search': search,
            'vehicle_type': vehicle_type,
        }
    }
    
    return render(request, 'inventory/alerts_list.html', context)

@login_required
@permission_required('edit_products')
@require_http_methods(["POST"])
def acknowledge_alert(request, alert_id):
    """Acknowledge an alert"""
    alert = get_object_or_404(InventoryAlert, id=alert_id)
    
    if alert.status == 'active':
        alert.status = 'acknowledged'
        alert.acknowledged_by = request.user
        alert.acknowledged_at = timezone.now()
        alert.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action='update',
            description=f'Acknowledged alert for {alert.product.name}',
            content_object=alert
        )
        
        messages.success(request, f'Alert for {alert.product.name} acknowledged.')
    else:
        messages.warning(request, 'Alert has already been acknowledged.')
    
    return JsonResponse({'status': 'success'})

@login_required
@permission_required('edit_products')
@require_http_methods(["POST"])
def resolve_alert(request, alert_id):
    """Resolve an alert"""
    alert = get_object_or_404(InventoryAlert, id=alert_id)
    
    alert.status = 'resolved'
    alert.acknowledged_by = request.user
    alert.acknowledged_at = timezone.now()
    alert.save()
    
    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        action='update',
        description=f'Resolved alert for {alert.product.name}',
        content_object=alert
    )
    
    messages.success(request, f'Alert for {alert.product.name} resolved.')
    return JsonResponse({'status': 'success'})

@login_required
@permission_required('edit_products')
@require_http_methods(["POST"])
def bulk_acknowledge_alerts(request):
    """Bulk acknowledge alerts"""
    alert_ids = request.POST.getlist('alert_ids')
    
    if alert_ids:
        alerts = InventoryAlert.objects.filter(id__in=alert_ids, status='active')
        count = alerts.update(
            status='acknowledged',
            acknowledged_by=request.user,
            acknowledged_at=timezone.now()
        )
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action='update',
            description=f'Bulk acknowledged {count} alerts'
        )
        
        messages.success(request, f'{count} alerts acknowledged successfully.')
    
    return redirect('inventory:alerts_list')

@login_required
@permission_required('view_stock_reports')
def purchase_requirements(request):
    """Generate purchase requirements report based on alerts"""
    # Get products that need reordering
    reorder_alerts = InventoryAlert.objects.filter(
        alert_type__in=['out_of_stock', 'low_stock', 'reorder'],
        status='active'
    ).select_related('product__category', 'product__brand')
    
    # Group by supplier (if we had supplier in product model)
    # For now, group by category and brand
    purchase_requirements = []
    
    for alert in reorder_alerts:
        product = alert.product
        
        # Calculate recommended quantity
        if product.current_stock <= 0:
            # Out of stock - order to maximum
            recommended_qty = product.maximum_stock
        elif product.current_stock <= product.minimum_stock:
            # Low stock - order to safe level
            recommended_qty = product.maximum_stock - product.current_stock
        else:
            # At reorder level - order standard quantity
            recommended_qty = product.reorder_level * 2
        
        total_cost = recommended_qty * product.cost_price
        
        purchase_requirements.append({
            'product': product,
            'alert': alert,
            'recommended_qty': recommended_qty,
            'total_cost': total_cost,
            'priority': 'HIGH' if alert.alert_type == 'out_of_stock' else 'MEDIUM'
        })
    
    # Sort by priority and total cost
    purchase_requirements.sort(key=lambda x: (x['priority'] == 'MEDIUM', -x['total_cost']))
    
    # Calculate totals
    total_items = len(purchase_requirements)
    total_cost = sum(req['total_cost'] for req in purchase_requirements)
    high_priority_count = sum(1 for req in purchase_requirements if req['priority'] == 'HIGH')
    
    context = {
        'purchase_requirements': purchase_requirements,
        'total_items': total_items,
        'total_cost': total_cost,
        'high_priority_count': high_priority_count,
    }
    
    return render(request, 'inventory/purchase_requirements.html', context)

@login_required
@permission_required('edit_products')
def refresh_alerts(request):
    """Manually refresh inventory alerts"""
    from django.core.management import call_command
    from io import StringIO
    
    try:
        # Capture command output
        out = StringIO()
        call_command('check_inventory_alerts', stdout=out)
        
        messages.success(request, 'Inventory alerts refreshed successfully.')
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action='system',
            description='Manual inventory alerts refresh'
        )
        
    except Exception as e:
        messages.error(request, f'Error refreshing alerts: {str(e)}')
    
    return redirect('inventory:alerts_dashboard')