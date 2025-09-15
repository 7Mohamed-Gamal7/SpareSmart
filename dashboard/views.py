from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Notification, SystemAlert, UserPreference, ActivityLog
from sales.models import Sale, Payment
from purchases.models import Purchase
from expenses.models import Expense
from inventory.models import Product, InventoryAlert
from accounts.models import User

@login_required
def home(request):
    """Dashboard home view with key metrics and charts"""
    
    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)
    
    # Sales Statistics
    today_sales = Sale.objects.filter(sale_date__date=today)
    week_sales = Sale.objects.filter(sale_date__date__gte=week_ago)
    month_sales = Sale.objects.filter(sale_date__date__gte=month_ago)
    
    sales_stats = {
        'today_count': today_sales.count(),
        'today_amount': today_sales.aggregate(total=Sum('total_amount'))['total'] or 0,
        'week_count': week_sales.count(),
        'week_amount': week_sales.aggregate(total=Sum('total_amount'))['total'] or 0,
        'month_count': month_sales.count(),
        'month_amount': month_sales.aggregate(total=Sum('total_amount'))['total'] or 0,
    }
    
    # Purchase Statistics
    month_purchases = Purchase.objects.filter(order_date__date__gte=month_ago)
    purchase_stats = {
        'month_count': month_purchases.count(),
        'month_amount': month_purchases.aggregate(total=Sum('total_amount'))['total'] or 0,
        'pending_count': Purchase.objects.filter(status='pending').count(),
    }
    
    # Expense Statistics
    month_expenses = Expense.objects.filter(expense_date__gte=month_ago)
    expense_stats = {
        'month_count': month_expenses.count(),
        'month_amount': month_expenses.aggregate(total=Sum('amount'))['total'] or 0,
        'pending_approval': Expense.objects.filter(status='pending', requires_approval=True).count(),
    }
    
    # Inventory Statistics
    inventory_stats = {
        'total_products': Product.objects.filter(is_active=True).count(),
        'low_stock_count': Product.objects.filter(
            current_stock__lte=models.F('reorder_level'),
            is_active=True
        ).count(),
        'out_of_stock_count': Product.objects.filter(
            current_stock=0,
            is_active=True
        ).count(),
        'total_value': Product.objects.filter(is_active=True).aggregate(
            total=Sum(models.F('current_stock') * models.F('cost_price'))
        )['total'] or 0,
    }
    
    # Recent Activities
    recent_activities = ActivityLog.objects.select_related('user').order_by('-timestamp')[:10]
    
    # Pending Items (for superuser, admin/manager roles)
    pending_items = {}
    if request.user.is_superuser or request.user.role in ['admin', 'manager']:
        pending_items = {
            'pending_expenses': Expense.objects.filter(status='pending', requires_approval=True).count(),
            'low_stock_alerts': InventoryAlert.objects.filter(status='active', alert_type='low_stock').count(),
            'overdue_payments': Sale.objects.filter(payment_status='overdue').count(),
        }
    
    # Charts data
    # Sales trend for last 7 days
    sales_trend = []
    for i in range(7):
        date = today - timedelta(days=i)
        day_sales = Sale.objects.filter(sale_date__date=date).aggregate(
            total=Sum('total_amount'))['total'] or 0
        sales_trend.append({
            'date': date.strftime('%Y-%m-%d'),
            'amount': float(day_sales)
        })
    sales_trend.reverse()
    
    # Top selling products
    top_products = Product.objects.annotate(
        total_sold=Sum('saleitem__quantity')
    ).filter(total_sold__gt=0).order_by('-total_sold')[:5]
    
    context = {
        'sales_stats': sales_stats,
        'purchase_stats': purchase_stats,
        'expense_stats': expense_stats,
        'inventory_stats': inventory_stats,
        'recent_activities': recent_activities,
        'pending_items': pending_items,
        'sales_trend': sales_trend,
        'top_products': top_products,
    }
    
    return render(request, 'dashboard/home.html', context)

@login_required
def notifications(request):
    """User notifications view"""
    user_notifications = request.user.notifications.order_by('-created_at')
    
    # Mark as read if requested
    if request.GET.get('mark_all_read'):
        user_notifications.filter(is_read=False).update(is_read=True, read_at=timezone.now())
        messages.success(request, 'All notifications marked as read.')
        return redirect('dashboard:notifications')
    
    context = {
        'notifications': user_notifications,
        'unread_count': user_notifications.filter(is_read=False).count(),
    }
    
    return render(request, 'dashboard/notifications.html', context)

@login_required
def mark_notification_read(request, notification_id):
    """Mark single notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('dashboard:notifications')

@login_required
def system_alerts(request):
    """System alerts view"""
    alerts = SystemAlert.objects.filter(
        status='active',
        start_date__lte=timezone.now()
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=timezone.now())
    )
    
    # Filter by user role if target_roles is specified
    user_alerts = []
    for alert in alerts:
        if not alert.target_roles or request.user.role in alert.target_roles:
            user_alerts.append(alert)
    
    context = {
        'alerts': user_alerts,
    }
    
    return render(request, 'dashboard/system_alerts.html', context)

@login_required
def user_preferences(request):
    """User preferences view"""
    try:
        preferences = request.user.preferences
    except UserPreference.DoesNotExist:
        preferences = UserPreference.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Update preferences
        preferences.theme = request.POST.get('theme', 'light')
        preferences.language = request.POST.get('language', 'en')
        preferences.timezone = request.POST.get('timezone', 'UTC')
        preferences.items_per_page = int(request.POST.get('items_per_page', 20))
        preferences.email_notifications = 'email_notifications' in request.POST
        preferences.push_notifications = 'push_notifications' in request.POST
        preferences.notification_sound = 'notification_sound' in request.POST
        preferences.save()
        
        messages.success(request, 'Preferences updated successfully.')
        return redirect('dashboard:preferences')
    
    context = {
        'preferences': preferences,
    }
    
    return render(request, 'dashboard/preferences.html', context)

@login_required
def activity_log(request):
    """Activity log view"""
    activities = ActivityLog.objects.select_related('user').order_by('-timestamp')
    
    # Filter by user if not superuser/admin/manager
    if not request.user.is_superuser and request.user.role not in ['admin', 'manager']:
        activities = activities.filter(user=request.user)

    # Filtering
    user_filter = request.GET.get('user')
    action_filter = request.GET.get('action')
    date_filter = request.GET.get('date')

    if user_filter and (request.user.is_superuser or request.user.role in ['admin', 'manager']):
        activities = activities.filter(user__username__icontains=user_filter)
    
    if action_filter:
        activities = activities.filter(action=action_filter)
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            activities = activities.filter(timestamp__date=filter_date)
        except ValueError:
            pass
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(activities, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'action_choices': ActivityLog.ACTION_CHOICES,
        'current_filters': {
            'user': user_filter,
            'action': action_filter,
            'date': date_filter,
        }
    }
    
    return render(request, 'dashboard/activity_log.html', context)