from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, F
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.template.loader import render_to_string
from decimal import Decimal
import json
from datetime import datetime, timedelta

from .models import Purchase, PurchaseItem, PurchasePayment
from .forms import (
    PurchaseForm, PurchaseItemFormSet, PurchaseReceivingForm,
    PurchasePaymentForm, PurchaseFilterForm, QuickPurchaseForm
)
from inventory.models import Product, Supplier, StockMovement
from accounts.models import User
from dashboard.models import ActivityLog
from accounts.views import permission_required


@login_required
@permission_required('view_purchases')
def purchase_list(request):
    """List all purchases with filtering and pagination"""
    purchases = Purchase.objects.select_related('supplier', 'created_by').prefetch_related('items')
    
    # Initialize filter form
    filter_form = PurchaseFilterForm(request.GET)
    
    # Apply filters
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        supplier = filter_form.cleaned_data.get('supplier')
        status = filter_form.cleaned_data.get('status')
        payment_status = filter_form.cleaned_data.get('payment_status')
        date_range = filter_form.cleaned_data.get('date_range')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        
        if search:
            purchases = purchases.filter(
                Q(purchase_number__icontains=search) |
                Q(supplier__name__icontains=search) |
                Q(supplier_invoice_number__icontains=search) |
                Q(supplier_reference__icontains=search)
            )
        
        if supplier:
            purchases = purchases.filter(supplier=supplier)
        
        if status:
            purchases = purchases.filter(status=status)
        
        if payment_status:
            purchases = purchases.filter(payment_status=payment_status)
        
        # Date filtering
        if date_range:
            today = timezone.now().date()
            if date_range == 'today':
                purchases = purchases.filter(order_date__date=today)
            elif date_range == 'week':
                week_start = today - timedelta(days=today.weekday())
                purchases = purchases.filter(order_date__date__gte=week_start)
            elif date_range == 'month':
                purchases = purchases.filter(order_date__month=today.month, order_date__year=today.year)
            elif date_range == 'quarter':
                quarter_start = datetime(today.year, ((today.month-1)//3)*3+1, 1).date()
                purchases = purchases.filter(order_date__date__gte=quarter_start)
            elif date_range == 'year':
                purchases = purchases.filter(order_date__year=today.year)
        
        if date_from:
            purchases = purchases.filter(order_date__date__gte=date_from)
        
        if date_to:
            purchases = purchases.filter(order_date__date__lte=date_to)
    
    # Sorting
    sort_by = request.GET.get('sort', 'order_date')
    if sort_by in ['order_date', 'total_amount', 'supplier__name', 'status']:
        if sort_by == 'order_date':
            purchases = purchases.order_by('-order_date')
        else:
            purchases = purchases.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(purchases, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    today = timezone.now().date()
    total_purchases = Purchase.objects.count()
    today_purchases = Purchase.objects.filter(order_date__date=today).count()
    pending_orders = Purchase.objects.filter(status__in=['pending', 'ordered']).count()
    
    # Calculate today's purchase amount
    today_amount = Purchase.objects.filter(
        order_date__date=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Calculate pending payments
    pending_payments = Purchase.objects.filter(
        payment_status__in=['unpaid', 'partial', 'overdue']
    ).aggregate(total=Sum('balance_amount'))['total'] or 0
    
    context = {
        'purchases': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'filter_form': filter_form,
        'total_purchases': total_purchases,
        'today_purchases': today_purchases,
        'pending_orders': pending_orders,
        'today_amount': today_amount,
        'pending_payments': pending_payments,
    }
    
    return render(request, 'purchases/purchase_list.html', context)


@login_required
@permission_required('add_purchases')
def purchase_create(request):
    """Create new purchase order"""
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    purchase = form.save(commit=False)
                    purchase.created_by = request.user
                    purchase.save()
                    
                    # Save items and calculate totals
                    subtotal = Decimal('0.00')
                    formset.instance = purchase
                    
                    for item_form in formset:
                        if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                            item = item_form.save(commit=False)
                            item.purchase = purchase
                            item.save()
                            subtotal += Decimal(str(item.total_cost))
                    
                    # Update purchase totals
                    purchase.subtotal = subtotal
                    purchase.total_amount = (
                        subtotal +
                        Decimal(str(purchase.tax_amount or 0)) +
                        Decimal(str(purchase.shipping_cost or 0)) -
                        Decimal(str(purchase.discount_amount or 0))
                    )
                    purchase.balance_amount = purchase.total_amount
                    purchase.save()
                    
                    # Log activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='create',
                        description=f'تم إنشاء أمر شراء: {purchase.purchase_number}',
                        content_object=purchase
                    )

                    messages.success(request, f'تم إنشاء أمر الشراء {purchase.purchase_number} بنجاح.')
                    return redirect('purchases:purchase_detail', purchase_id=purchase.id)
                    
            except Exception as e:
                messages.error(request, f'خطأ في إنشاء أمر الشراء: {str(e)}')
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet()

    context = {
        'form': form,
        'formset': formset,
        'title': 'إنشاء أمر شراء جديد',
        'action': 'إنشاء'
    }
    
    return render(request, 'purchases/purchase_form.html', context)


@login_required
@permission_required('view_purchases')
def purchase_detail(request, purchase_id):
    """View purchase order details"""
    purchase = get_object_or_404(
        Purchase.objects.select_related('supplier', 'created_by', 'updated_by', 'received_by')
        .prefetch_related('items__product', 'payments'),
        id=purchase_id
    )
    
    # Get payments
    payments = purchase.payments.all().order_by('-payment_date')
    
    # Get recent stock movements related to this purchase
    stock_movements = StockMovement.objects.filter(
        reference__icontains=purchase.purchase_number
    ).select_related('product', 'user').order_by('-created_at')[:10]
    
    context = {
        'purchase': purchase,
        'payments': payments,
        'stock_movements': stock_movements,
    }
    
    return render(request, 'purchases/purchase_detail.html', context)


@login_required
@permission_required('change_purchases')
def purchase_update(request, purchase_id):
    """Update purchase order"""
    purchase = get_object_or_404(Purchase, id=purchase_id)
    
    # Check if purchase can be edited
    if purchase.status in ['received', 'cancelled']:
        messages.error(request, 'Cannot edit a received or cancelled purchase order.')
        return redirect('purchases:purchase_detail', purchase_id=purchase.id)
    
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseItemFormSet(request.POST, instance=purchase)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    updated_purchase = form.save(commit=False)
                    updated_purchase.updated_by = request.user
                    updated_purchase.save()
                    
                    # Save items and recalculate totals
                    subtotal = Decimal('0.00')
                    formset.save()
                    
                    for item in updated_purchase.items.all():
                        subtotal += Decimal(str(item.total_cost))
                    
                    # Update purchase totals
                    updated_purchase.subtotal = subtotal
                    updated_purchase.total_amount = (
                        subtotal +
                        Decimal(str(updated_purchase.tax_amount or 0)) +
                        Decimal(str(updated_purchase.shipping_cost or 0)) -
                        Decimal(str(updated_purchase.discount_amount or 0))
                    )
                    updated_purchase.save()
                    
                    # Log activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='update',
                        description=f'Updated purchase order: {updated_purchase.purchase_number}',
                        content_object=updated_purchase
                    )
                    
                    messages.success(request, f'Purchase order {updated_purchase.purchase_number} updated successfully.')
                    return redirect('purchases:purchase_detail', purchase_id=updated_purchase.id)
                    
            except Exception as e:
                messages.error(request, f'Error updating purchase order: {str(e)}')
    else:
        form = PurchaseForm(instance=purchase)
        formset = PurchaseItemFormSet(instance=purchase)
    
    context = {
        'form': form,
        'formset': formset,
        'purchase': purchase,
        'title': f'Edit Purchase Order: {purchase.purchase_number}',
        'action': 'Update'
    }
    
    return render(request, 'purchases/purchase_form.html', context)


@login_required
@permission_required('receive_purchases')
def purchase_receive(request, purchase_id):
    """Receive goods against purchase order"""
    purchase = get_object_or_404(Purchase, id=purchase_id)
    
    if purchase.status == 'received':
        messages.info(request, 'This purchase order has already been fully received.')
        return redirect('purchases:purchase_detail', purchase_id=purchase.id)
    
    if request.method == 'POST':
        form = PurchaseReceivingForm(purchase, request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    has_updates = False
                    
                    for field_name, value in form.cleaned_data.items():
                        if field_name.startswith('receive_qty_') and value and value > 0:
                            item_id = field_name.split('_')[-1]
                            item = get_object_or_404(PurchaseItem, id=item_id, purchase=purchase)
                            
                            # Update received quantity
                            item.quantity_received += value
                            
                            # Get quality check data
                            quality_passed = form.cleaned_data.get(f'quality_check_{item_id}', True)
                            quality_notes = form.cleaned_data.get(f'quality_notes_{item_id}', '')
                            
                            item.quality_check_passed = quality_passed
                            if quality_notes:
                                item.quality_notes = quality_notes
                            
                            item.save()
                            
                            # Update product stock if quality check passed
                            if quality_passed:
                                item.product.current_stock += value
                                item.product.save()
                                
                                # Create stock movement record
                                StockMovement.objects.create(
                                    product=item.product,
                                    movement_type='in',
                                    quantity=value,
                                    reference=f'Purchase {purchase.purchase_number}',
                                    user=request.user,
                                    notes=f'Received from {purchase.supplier.name}'
                                )
                            
                            has_updates = True
                    
                    if has_updates:
                        # Update purchase status
                        all_received = all(item.is_fully_received for item in purchase.items.all())
                        any_received = any(item.quantity_received > 0 for item in purchase.items.all())
                        
                        if all_received:
                            purchase.status = 'received'
                            purchase.actual_delivery_date = timezone.now().date()
                        elif any_received:
                            purchase.status = 'partial_received'
                        
                        purchase.received_by = request.user
                        purchase.save()
                        
                        # Log activity
                        ActivityLog.objects.create(
                            user=request.user,
                            action='receive',
                            description=f'Received goods for purchase: {purchase.purchase_number}',
                            content_object=purchase
                        )
                        
                        messages.success(request, 'Goods received successfully.')
                        return redirect('purchases:purchase_detail', purchase_id=purchase.id)
                    else:
                        messages.warning(request, 'No items were selected for receiving.')
                        
            except Exception as e:
                messages.error(request, f'Error receiving goods: {str(e)}')
    else:
        form = PurchaseReceivingForm(purchase)
    
    context = {
        'form': form,
        'purchase': purchase,
    }
    
    return render(request, 'purchases/purchase_receive.html', context)


@login_required
@permission_required('view_purchases')
def purchase_invoice(request, purchase_id):
    """View purchase invoice"""
    purchase = get_object_or_404(
        Purchase.objects.select_related('supplier', 'created_by')
        .prefetch_related('items__product', 'payments'),
        id=purchase_id
    )
    
    # Get payments
    payments = purchase.payments.all().order_by('-payment_date')
    
    context = {
        'purchase': purchase,
        'payments': payments,
    }
    
    return render(request, 'purchases/purchase_invoice.html', context)


@login_required
@permission_required('view_purchases')
def purchase_payment_list(request, purchase_id):
    """List payments for a purchase"""
    purchase = get_object_or_404(Purchase, id=purchase_id)
    payments = purchase.payments.all().order_by('-payment_date')
    
    context = {
        'purchase': purchase,
        'payments': payments,
    }
    
    return render(request, 'purchases/payment_list.html', context)


@login_required
@permission_required('add_purchase_payments')
def purchase_payment_create(request, purchase_id):
    """Create payment for purchase"""
    purchase = get_object_or_404(Purchase, id=purchase_id)
    
    if purchase.balance_amount <= 0:
        messages.info(request, 'This purchase is already fully paid.')
        return redirect('purchases:purchase_detail', purchase_id=purchase.id)
    
    if request.method == 'POST':
        form = PurchasePaymentForm(purchase, request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    payment = form.save(commit=False)
                    payment.purchase = purchase
                    payment.paid_by = request.user
                    payment.save()
                    
                    # Update purchase paid amount
                    purchase.paid_amount += payment.amount
                    purchase.save()  # This will trigger balance calculation in model
                    
                    # Log activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='payment',
                        description=f'Recorded payment of ${payment.amount} for purchase {purchase.purchase_number}',
                        content_object=purchase
                    )
                    
                    messages.success(request, f'Payment of ${payment.amount:.2f} recorded successfully.')
                    return redirect('purchases:purchase_detail', purchase_id=purchase.id)
                    
            except Exception as e:
                messages.error(request, f'Error recording payment: {str(e)}')
    else:
        form = PurchasePaymentForm(purchase)
    
    context = {
        'form': form,
        'purchase': purchase,
    }
    
    return render(request, 'purchases/payment_form.html', context)


@login_required
@permission_required('add_purchases')
def quick_purchase(request):
    """Quick purchase order creation"""
    if request.method == 'POST':
        form = QuickPurchaseForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create purchase
                    purchase = Purchase.objects.create(
                        supplier=form.cleaned_data['supplier'],
                        payment_due_date=form.cleaned_data.get('payment_due_date'),
                        notes=form.cleaned_data.get('notes'),
                        created_by=request.user
                    )
                    
                    # Create items
                    subtotal = Decimal('0.00')
                    products_data = form.cleaned_data['products']
                    
                    for product_data in products_data:
                        product = get_object_or_404(Product, id=product_data['product_id'])
                        quantity = int(product_data['quantity'])
                        unit_cost = Decimal(str(product_data['unit_cost']))
                        
                        item = PurchaseItem.objects.create(
                            purchase=purchase,
                            product=product,
                            quantity_ordered=quantity,
                            unit_cost=unit_cost
                        )
                        subtotal += Decimal(str(item.total_cost))
                    
                    # Update purchase totals
                    purchase.subtotal = subtotal
                    purchase.total_amount = subtotal
                    purchase.balance_amount = subtotal
                    purchase.save()
                    
                    # Log activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='create',
                        description=f'Created quick purchase order: {purchase.purchase_number}',
                        content_object=purchase
                    )
                    
                    messages.success(request, f'Quick purchase order {purchase.purchase_number} created successfully.')
                    return redirect('purchases:purchase_detail', purchase_id=purchase.id)
                    
            except Exception as e:
                messages.error(request, f'Error creating quick purchase: {str(e)}')
    else:
        form = QuickPurchaseForm()
    
    # Get recent suppliers for quick selection
    recent_suppliers = Supplier.objects.filter(is_active=True).order_by('-updated_at')[:10]
    
    context = {
        'form': form,
        'recent_suppliers': recent_suppliers,
    }
    
    return render(request, 'purchases/quick_purchase.html', context)


# AJAX Views
@login_required
def get_product_cost(request):
    """AJAX endpoint to get product cost price"""
    product_id = request.GET.get('product_id')
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            return JsonResponse({
                'cost_price': float(product.cost_price),
                'current_stock': product.current_stock,
                'minimum_stock': product.minimum_stock,
            })
        except Product.DoesNotExist:
            pass
    
    return JsonResponse({'error': 'Product not found'}, status=404)

@login_required
def purchase_return_list(request):
    return render(request, 'purchases/return_list.html', {'returns': []})

@login_required
def purchase_return_create(request, purchase_id):
    messages.info(request, 'Purchase return feature coming soon!')
    return redirect('purchases:purchase_return_list')