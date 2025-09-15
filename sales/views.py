from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, F
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.template.loader import get_template
from django.utils import timezone
from accounts.views import permission_required
from .models import Sale, SaleItem, Payment, Installment, InstallmentPayment
from .forms import (
    SaleForm, SaleItemInlineFormSet, PaymentForm, InstallmentPlanForm,
    SaleFilterForm, QuickSaleForm, InstallmentPaymentForm
)
from inventory.models import Product, Customer
from dashboard.models import ActivityLog
from datetime import datetime, timedelta
import json
from decimal import Decimal

@login_required
@permission_required('view_sales')
def sale_list(request):
    """List all sales with filtering and pagination"""
    sales = Sale.objects.select_related('customer', 'created_by').prefetch_related('items__product').all()
    filter_form = SaleFilterForm(request.GET)
    
    # Apply filters
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        customer = filter_form.cleaned_data.get('customer')
        sale_type = filter_form.cleaned_data.get('sale_type')
        status = filter_form.cleaned_data.get('status')
        payment_status = filter_form.cleaned_data.get('payment_status')
        date_range = filter_form.cleaned_data.get('date_range')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        
        if search:
            sales = sales.filter(
                Q(sale_number__icontains=search) |
                Q(customer__name__icontains=search) |
                Q(customer__phone__icontains=search)
            )
        
        if customer:
            sales = sales.filter(customer=customer)
        
        if sale_type:
            sales = sales.filter(sale_type=sale_type)
        
        if status:
            sales = sales.filter(status=status)
        
        if payment_status:
            sales = sales.filter(payment_status=payment_status)
        
        # Date range filtering
        if date_range:
            today = timezone.now().date()
            if date_range == 'today':
                sales = sales.filter(sale_date__date=today)
            elif date_range == 'yesterday':
                yesterday = today - timedelta(days=1)
                sales = sales.filter(sale_date__date=yesterday)
            elif date_range == 'this_week':
                week_start = today - timedelta(days=today.weekday())
                sales = sales.filter(sale_date__date__gte=week_start)
            elif date_range == 'this_month':
                sales = sales.filter(sale_date__year=today.year, sale_date__month=today.month)
            elif date_range == 'last_month':
                last_month = today.replace(day=1) - timedelta(days=1)
                sales = sales.filter(sale_date__year=last_month.year, sale_date__month=last_month.month)
        
        if date_from:
            sales = sales.filter(sale_date__date__gte=date_from)
        
        if date_to:
            sales = sales.filter(sale_date__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(sales, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    today = timezone.now().date()
    total_sales = sales.count()
    today_sales = Sale.objects.filter(sale_date__date=today).aggregate(
        count=Count('id'), total=Sum('total_amount'))['count'] or 0
    today_revenue = Sale.objects.filter(sale_date__date=today).aggregate(
        total=Sum('total_amount'))['total'] or 0
    pending_payments = Sale.objects.filter(payment_status__in=['unpaid', 'partial']).aggregate(
        total=Sum('balance_amount'))['total'] or 0
    
    context = {
        'sales': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'filter_form': filter_form,
        'total_sales': total_sales,
        'today_sales': today_sales,
        'today_revenue': today_revenue,
        'pending_payments': pending_payments,
    }
    
    return render(request, 'sales/sale_list.html', context)

@login_required
@permission_required('create_sales')
def sale_create(request):
    """Create new sale"""
    if request.method == 'POST':
        form = SaleForm(request.POST)
        formset = SaleItemInlineFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    sale = form.save(commit=False)
                    sale.created_by = request.user
                    sale.save()
                    
                    formset.instance = sale
                    sale_items = formset.save()
                    
                    # Calculate totals
                    subtotal = sum(item.total_price for item in sale_items)
                    sale.subtotal = subtotal
                    sale.total_amount = subtotal - sale.discount_amount
                    sale.save()
                    
                    # Update product stock
                    for item in sale_items:
                        product = item.product
                        product.current_stock -= item.quantity
                        product.save()
                        
                        # Create stock movement
                        from inventory.models import StockMovement
                        StockMovement.objects.create(
                            product=product,
                            movement_type='out',
                            quantity=item.quantity,
                            unit_cost=item.cost_price,
                            reference_number=sale.sale_number,
                            notes=f'Sale to {sale.customer.name}',
                            created_by=request.user
                        )
                    
                    # Log activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='create',
                        description=f'Created sale: {sale.sale_number} for {sale.customer.name}',
                        content_object=sale
                    )
                    
                    messages.success(request, f'Sale {sale.sale_number} created successfully.')
                    return redirect('sales:sale_detail', sale_id=sale.id)
                    
            except Exception as e:
                messages.error(request, f'Error creating sale: {str(e)}')
    else:
        form = SaleForm()
        formset = SaleItemInlineFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'عملية بيع جديدة',
        'action': 'إنشاء'
    }
    
    return render(request, 'sales/sale_form.html', context)

@login_required
@permission_required('view_sales')
def sale_detail(request, sale_id):
    """View sale details"""
    sale = get_object_or_404(Sale, id=sale_id)
    payments = sale.payments.all().order_by('-payment_date')
    
    # Check if sale has installment plan
    installment_plan = getattr(sale, 'installment_plan', None)
    installment_payments = []
    if installment_plan:
        installment_payments = installment_plan.installment_payments.all().order_by('installment_number')
    
    context = {
        'sale': sale,
        'payments': payments,
        'installment_plan': installment_plan,
        'installment_payments': installment_payments,
    }
    
    return render(request, 'sales/sale_detail.html', context)

@login_required
@permission_required('edit_sales')
def sale_update(request, sale_id):
    """Update sale"""
    sale = get_object_or_404(Sale, id=sale_id)
    
    # Don't allow editing completed sales
    if sale.status == 'completed':
        messages.error(request, 'Cannot edit completed sales.')
        return redirect('sales:sale_detail', sale_id=sale.id)
    
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        formset = SaleItemInlineFormSet(request.POST, instance=sale)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Restore stock for deleted items
                    for form_item in formset.deleted_forms:
                        if form_item.instance.pk:
                            product = form_item.instance.product
                            product.current_stock += form_item.instance.quantity
                            product.save()
                    
                    updated_sale = form.save(commit=False)
                    updated_sale.updated_by = request.user
                    updated_sale.save()
                    
                    sale_items = formset.save()
                    
                    # Recalculate totals
                    subtotal = sum(item.total_price for item in sale.items.all())
                    updated_sale.subtotal = subtotal
                    updated_sale.total_amount = subtotal - updated_sale.discount_amount
                    updated_sale.save()
                    
                    # Log activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='update',
                        description=f'Updated sale: {updated_sale.sale_number}',
                        content_object=updated_sale
                    )
                    
                    messages.success(request, f'Sale {updated_sale.sale_number} updated successfully.')
                    return redirect('sales:sale_detail', sale_id=updated_sale.id)
                    
            except Exception as e:
                messages.error(request, f'Error updating sale: {str(e)}')
    else:
        form = SaleForm(instance=sale)
        formset = SaleItemInlineFormSet(instance=sale)
    
    context = {
        'form': form,
        'formset': formset,
        'sale': sale,
        'title': f'Edit Sale: {sale.sale_number}',
        'action': 'Update'
    }
    
    return render(request, 'sales/sale_form.html', context)

@login_required
@permission_required('view_sales')
def sale_invoice(request, sale_id):
    """Generate and display invoice"""
    sale = get_object_or_404(Sale, id=sale_id)
    
    context = {
        'sale': sale,
        'company_info': {
            'name': 'SpareSmart Store',
            'address': 'Your Store Address',
            'phone': 'Your Phone Number',
            'email': 'info@sparesmart.com',
        }
    }
    
    return render(request, 'sales/invoice.html', context)

@login_required
@permission_required('view_sales')
def sale_print(request, sale_id):
    """Print-friendly invoice view"""
    sale = get_object_or_404(Sale, id=sale_id)
    
    context = {
        'sale': sale,
        'company_info': {
            'name': 'SpareSmart Store',
            'address': 'Your Store Address',
            'phone': 'Your Phone Number',
            'email': 'info@sparesmart.com',
        }
    }
    
    return render(request, 'sales/invoice_print.html', context)

@login_required
@permission_required('process_payments')
def payment_create(request, sale_id):
    """Record payment for a sale"""
    sale = get_object_or_404(Sale, id=sale_id)
    
    if sale.balance_amount <= 0:
        messages.error(request, 'This sale is already fully paid.')
        return redirect('sales:sale_detail', sale_id=sale.id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, sale=sale)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    payment = form.save(commit=False)
                    payment.sale = sale
                    payment.received_by = request.user
                    payment.save()
                    
                    # Update sale paid amount
                    sale.paid_amount += payment.amount
                    sale.save()  # This will trigger payment status update
                    
                    # Log activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='create',
                        description=f'Recorded payment: {payment.payment_number} for sale {sale.sale_number}',
                        content_object=payment
                    )
                    
                    messages.success(request, f'Payment of ${payment.amount} recorded successfully.')
                    return redirect('sales:sale_detail', sale_id=sale.id)
                    
            except Exception as e:
                messages.error(request, f'Error recording payment: {str(e)}')
    else:
        form = PaymentForm(sale=sale)
    
    context = {
        'form': form,
        'sale': sale,
        'title': f'Record Payment for Sale {sale.sale_number}'
    }
    
    return render(request, 'sales/payment_form.html', context)

@login_required
@permission_required('manage_installments')
def installment_list(request):
    """List all installment plans with filtering"""
    installments = Installment.objects.select_related('sale__customer').all()
    
    # Filtering
    status_filter = request.GET.get('status')
    customer_filter = request.GET.get('customer')
    
    if status_filter:
        installments = installments.filter(status=status_filter)
    
    if customer_filter:
        installments = installments.filter(sale__customer__name__icontains=customer_filter)
    
    # Pagination
    paginator = Paginator(installments, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_installments = installments.count()
    active_installments = installments.filter(status='active').count()
    overdue_payments = InstallmentPayment.objects.filter(
        status='overdue', installment_plan__status='active').count()
    total_outstanding = installments.filter(status='active').aggregate(
        total=Sum('total_amount'))['total'] or 0
    
    context = {
        'installments': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_installments': total_installments,
        'active_installments': active_installments,
        'overdue_payments': overdue_payments,
        'total_outstanding': total_outstanding,
        'status_choices': Installment.STATUS_CHOICES,
    }
    
    return render(request, 'sales/installment_list.html', context)

@login_required
@permission_required('manage_installments')
def installment_detail(request, installment_id):
    """View installment plan details"""
    installment = get_object_or_404(Installment, id=installment_id)
    payments = installment.installment_payments.all().order_by('installment_number')
    
    context = {
        'installment': installment,
        'payments': payments,
    }
    
    return render(request, 'sales/installment_detail.html', context)

@login_required
@permission_required('manage_installments')
def installment_payment(request, installment_payment_id):
    """Record installment payment"""
    installment_payment = get_object_or_404(InstallmentPayment, id=installment_payment_id)
    
    if installment_payment.status == 'paid':
        messages.error(request, 'This installment is already paid.')
        return redirect('sales:installment_detail', installment_id=installment_payment.installment_plan.id)
    
    if request.method == 'POST':
        form = InstallmentPaymentForm(request.POST, instance=installment_payment)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    payment = form.save(commit=False)
                    payment.received_by = request.user
                    payment.save()
                    
                    # Log activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='update',
                        description=f'Recorded installment payment for {installment_payment.installment_plan.sale.sale_number}',
                        content_object=payment
                    )
                    
                    messages.success(request, f'Installment payment of ${payment.paid_amount} recorded successfully.')
                    return redirect('sales:installment_detail', installment_id=installment_payment.installment_plan.id)
                    
            except Exception as e:
                messages.error(request, f'Error recording installment payment: {str(e)}')
    else:
        form = InstallmentPaymentForm(instance=installment_payment)
    
    context = {
        'form': form,
        'installment_payment': installment_payment,
        'title': f'Record Installment Payment #{installment_payment.installment_number}'
    }
    
    return render(request, 'sales/installment_payment_form.html', context)

@login_required
@permission_required('create_sales')
def quick_sale(request):
    """Quick sale for simple cash transactions"""
    if request.method == 'POST':
        form = QuickSaleForm(request.POST)
        
        if form.is_valid():
            try:
                sale = form.create_sale(request.user)
                
                # Log activity
                ActivityLog.objects.create(
                    user=request.user,
                    action='create',
                    description=f'Created quick sale: {sale.sale_number}',
                    content_object=sale
                )
                
                messages.success(request, f'Quick sale {sale.sale_number} completed successfully.')
                return redirect('sales:sale_detail', sale_id=sale.id)
                
            except Exception as e:
                messages.error(request, f'Error creating quick sale: {str(e)}')
    else:
        form = QuickSaleForm()
    
    context = {
        'form': form,
        'title': 'Quick Sale'
    }
    
    return render(request, 'sales/quick_sale.html', context)

@login_required
@permission_required('view_sales')
def get_product_price(request):
    """AJAX endpoint to get product price"""
    product_id = request.GET.get('product_id')
    
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            return JsonResponse({
                'success': True,
                'price': str(product.selling_price),
                'stock': product.current_stock,
                'cost_price': str(product.cost_price)
            })
        except Product.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})