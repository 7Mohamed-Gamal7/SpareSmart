from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg, Q, F
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import json
import csv

from sales.models import Sale, SaleItem, Payment, Installment, InstallmentPayment
from inventory.models import Product, Category, Brand, Customer, Supplier
from purchases.models import Purchase, PurchaseItem
from expenses.models import Expense
from accounts.views import permission_required

@login_required
def reports_home(request):
    return render(request, 'reports/home.html', {})

@login_required
def generate_report(request):
    messages.info(request, 'Report generation feature coming soon!')
    return redirect('reports:reports_home')

@login_required
def report_template_list(request):
    return render(request, 'reports/template_list.html', {'templates': []})

@login_required
def report_template_create(request):
    messages.info(request, 'Report template creation feature coming soon!')
    return redirect('reports:report_template_list')

@login_required
def report_template_detail(request, template_id):
    messages.info(request, 'Report template detail feature coming soon!')
    return redirect('reports:report_template_list')

@login_required
def generated_report_list(request):
    return render(request, 'reports/generated_list.html', {'reports': []})

@login_required
def generated_report_detail(request, report_id):
    messages.info(request, 'Generated report detail feature coming soon!')
    return redirect('reports:generated_report_list')

@login_required
def download_report(request, report_id):
    messages.info(request, 'Report download feature coming soon!')
    return redirect('reports:generated_report_list')

@login_required
@permission_required('view_reports')
def sales_report(request):
    """Comprehensive sales report with analytics"""
    # Date filtering
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    date_range = request.GET.get('date_range', 'this_month')
    
    # Set default date range
    today = timezone.now().date()
    if date_range == 'today':
        date_from = date_to = today
    elif date_range == 'yesterday':
        date_from = date_to = today - timedelta(days=1)
    elif date_range == 'this_week':
        date_from = today - timedelta(days=today.weekday())
        date_to = today
    elif date_range == 'last_week':
        date_from = today - timedelta(days=today.weekday() + 7)
        date_to = today - timedelta(days=today.weekday() + 1)
    elif date_range == 'this_month':
        date_from = today.replace(day=1)
        date_to = today
    elif date_range == 'last_month':
        last_month = today.replace(day=1) - timedelta(days=1)
        date_from = last_month.replace(day=1)
        date_to = last_month
    elif date_range == 'this_year':
        date_from = today.replace(month=1, day=1)
        date_to = today
    elif date_range == 'custom' and date_from and date_to:
        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
    else:
        date_from = today.replace(day=1)
        date_to = today
    
    # Base queryset
    sales = Sale.objects.filter(
        sale_date__date__gte=date_from,
        sale_date__date__lte=date_to
    ).select_related('customer', 'created_by')
    
    # Additional filters
    customer_id = request.GET.get('customer')
    sale_type = request.GET.get('sale_type')
    payment_status = request.GET.get('payment_status')
    salesperson_id = request.GET.get('salesperson')
    
    if customer_id:
        sales = sales.filter(customer_id=customer_id)
    if sale_type:
        sales = sales.filter(sale_type=sale_type)
    if payment_status:
        sales = sales.filter(payment_status=payment_status)
    if salesperson_id:
        sales = sales.filter(created_by_id=salesperson_id)
    
    # Calculate summary statistics
    summary = sales.aggregate(
        total_sales=Sum('total_amount'),
        total_paid=Sum('paid_amount'),
        total_balance=Sum('balance_amount'),
        total_profit=Sum(F('items__unit_price') - F('items__cost_price')) * F('items__quantity'),
        count=Count('id'),
        avg_sale=Avg('total_amount')
    )
    
    # Sales by type
    sales_by_type = sales.values('sale_type').annotate(
        count=Count('id'),
        total=Sum('total_amount')
    ).order_by('sale_type')
    
    # Sales by payment status
    sales_by_payment = sales.values('payment_status').annotate(
        count=Count('id'),
        total=Sum('total_amount')
    ).order_by('payment_status')
    
    # Top customers
    top_customers = sales.values('customer__name', 'customer_id').annotate(
        total_sales=Sum('total_amount'),
        count=Count('id')
    ).order_by('-total_sales')[:10]
    
    # Top salespeople
    top_salespeople = sales.values('created_by__first_name', 'created_by__last_name', 'created_by_id').annotate(
        total_sales=Sum('total_amount'),
        count=Count('id')
    ).order_by('-total_sales')[:10]
    
    # Daily sales trend (last 30 days for chart)
    daily_sales = []
    for i in range(30):
        day = today - timedelta(days=i)
        day_sales = Sale.objects.filter(
            sale_date__date=day
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        daily_sales.append({
            'date': day.strftime('%Y-%m-%d'),
            'total': float(day_sales['total'] or 0),
            'count': day_sales['count'] or 0
        })
    daily_sales.reverse()
    
    # Export functionality
    export_format = request.GET.get('export')
    if export_format == 'csv':
        return export_sales_csv(sales, date_from, date_to)
    elif export_format == 'json':
        return export_sales_json(sales)
    
    # Pagination for detailed sales list
    paginator = Paginator(sales.order_by('-sale_date'), 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'summary': summary,
        'sales_by_type': sales_by_type,
        'sales_by_payment': sales_by_payment,
        'top_customers': top_customers,
        'top_salespeople': top_salespeople,
        'daily_sales_json': json.dumps(daily_sales),
        'page_obj': page_obj,
        'date_from': date_from,
        'date_to': date_to,
        'date_range': date_range,
        'customers': Customer.objects.filter(is_active=True).order_by('name'),
        'salespeople': Customer.objects.none(),  # Will be properly implemented
        'filters': {
            'customer': customer_id,
            'sale_type': sale_type,
            'payment_status': payment_status,
            'salesperson': salesperson_id,
        }
    }
    
    return render(request, 'reports/sales_report.html', context)

def export_sales_csv(sales, date_from, date_to):
    """Export sales data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sales_report_{date_from}_to_{date_to}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Sale Number', 'Date', 'عميل', 'Type', 'Total Amount', 
        'Paid Amount', 'Balance', 'Payment Status', 'Salesperson'
    ])
    
    for sale in sales:
        writer.writerow([
            sale.sale_number,
            sale.sale_date.strftime('%Y-%m-%d %H:%M'),
            sale.customer.name,
            sale.get_sale_type_display(),
            sale.total_amount,
            sale.paid_amount,
            sale.balance_amount,
            sale.get_payment_status_display(),
            sale.created_by.get_full_name()
        ])
    
    return response

def export_sales_json(sales):
    """Export sales data to JSON"""
    data = []
    for sale in sales:
        data.append({
            'sale_number': sale.sale_number,
            'date': sale.sale_date.isoformat(),
            'customer': sale.customer.name,
            'type': sale.sale_type,
            'total_amount': float(sale.total_amount),
            'paid_amount': float(sale.paid_amount),
            'balance_amount': float(sale.balance_amount),
            'payment_status': sale.payment_status,
            'salesperson': sale.created_by.get_full_name()
        })
    
    response = JsonResponse({'sales': data})
    response['Content-Disposition'] = 'attachment; filename="sales_report.json"'
    return response

@login_required
def purchases_report(request):
    messages.info(request, 'Purchases report feature coming soon!')
    return redirect('reports:reports_home')

@login_required
@permission_required('view_reports')
def inventory_report(request):
    """Comprehensive inventory report"""
    # Filters
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    vehicle_type = request.GET.get('vehicle_type')
    stock_status = request.GET.get('stock_status')
    sort_by = request.GET.get('sort_by', 'name')
    
    # Base queryset
    products = Product.objects.select_related('category', 'brand').filter(is_active=True)
    
    # Apply filters
    if category_id:
        products = products.filter(category_id=category_id)
    if brand_id:
        products = products.filter(brand_id=brand_id)
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
        elif stock_status == 'overstock':
            products = products.filter(current_stock__gt=F('maximum_stock'))
        elif stock_status == 'normal':
            products = products.filter(
                current_stock__gt=F('reorder_level'),
                current_stock__lte=F('maximum_stock')
            )
    
    # Sorting
    if sort_by == 'stock_value':
        products = products.annotate(
            stock_value=F('current_stock') * F('cost_price')
        ).order_by('-stock_value')
    elif sort_by == 'profit_margin':
        products = products.annotate(
            profit_margin=((F('selling_price') - F('cost_price')) / F('cost_price')) * 100
        ).order_by('-profit_margin')
    elif sort_by == 'stock_level':
        products = products.order_by('-current_stock')
    else:
        products = products.order_by('name')
    
    # Calculate summary statistics
    inventory_summary = products.aggregate(
        total_products=Count('id'),
        total_stock_value=Sum(F('current_stock') * F('cost_price')),
        total_selling_value=Sum(F('current_stock') * F('selling_price')),
        total_items=Sum('current_stock'),
        avg_profit_margin=Avg((F('selling_price') - F('cost_price')) / F('cost_price') * 100)
    )
    
    # Stock status breakdown
    stock_status_breakdown = {
        'out_of_stock': products.filter(current_stock=0).count(),
        'low_stock': products.filter(
            current_stock__gt=0,
            current_stock__lte=F('reorder_level')
        ).count(),
        'normal_stock': products.filter(
            current_stock__gt=F('reorder_level'),
            current_stock__lte=F('maximum_stock')
        ).count(),
        'overstock': products.filter(current_stock__gt=F('maximum_stock')).count(),
    }
    
    # Top products by value
    top_products_by_value = products.annotate(
        stock_value=F('current_stock') * F('cost_price')
    ).order_by('-stock_value')[:10]
    
    # Category breakdown
    category_breakdown = products.values('category__name', 'category__vehicle_type').annotate(
        product_count=Count('id'),
        total_stock=Sum('current_stock'),
        total_value=Sum(F('current_stock') * F('cost_price'))
    ).order_by('-total_value')
    
    # Brand breakdown
    brand_breakdown = products.filter(brand__isnull=False).values('brand__name').annotate(
        product_count=Count('id'),
        total_stock=Sum('current_stock'),
        total_value=Sum(F('current_stock') * F('cost_price'))
    ).order_by('-total_value')[:10]
    
    # Export functionality
    export_format = request.GET.get('export')
    if export_format == 'csv':
        return export_inventory_csv(products)
    
    # Pagination
    paginator = Paginator(products, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'inventory_summary': inventory_summary,
        'stock_status_breakdown': stock_status_breakdown,
        'top_products_by_value': top_products_by_value,
        'category_breakdown': category_breakdown,
        'brand_breakdown': brand_breakdown,
        'page_obj': page_obj,
        'categories': Category.objects.all().order_by('name'),
        'brands': Brand.objects.all().order_by('name'),
        'vehicle_types': Category.VEHICLE_TYPE_CHOICES,
        'filters': {
            'category': category_id,
            'brand': brand_id,
            'vehicle_type': vehicle_type,
            'stock_status': stock_status,
            'sort_by': sort_by,
        }
    }
    
    return render(request, 'reports/inventory_report.html', context)

def export_inventory_csv(products):
    """Export inventory data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'SKU', 'Name', 'فئة', 'Brand', 'Current Stock', 'Min Stock', 
        'إعادة ترتيب المستوى', 'Max Stock', 'Cost Price', 'Selling Price', 
        'Stock Value', 'Profit Margin %'
    ])
    
    for product in products:
        profit_margin = 0
        if product.cost_price > 0:
            profit_margin = ((product.selling_price - product.cost_price) / product.cost_price) * 100
        
        writer.writerow([
            product.sku,
            product.name,
            product.category.name,
            product.brand.name if product.brand else '',
            product.current_stock,
            product.minimum_stock,
            product.reorder_level,
            product.maximum_stock,
            product.cost_price,
            product.selling_price,
            product.current_stock * product.cost_price,
            f"{profit_margin:.2f}%"
        ])
    
    return response

@login_required
def expenses_report(request):
    messages.info(request, 'Expenses report feature coming soon!')
    return redirect('reports:reports_home')

@login_required
def profit_loss_report(request):
    messages.info(request, 'Profit & Loss report feature coming soon!')
    return redirect('reports:reports_home')

@login_required
def installments_report(request):
    messages.info(request, 'Installments report feature coming soon!')
    return redirect('reports:reports_home')