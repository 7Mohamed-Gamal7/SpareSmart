from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', views.product_update, name='product_update'),
    path('products/bulk-action/', views.bulk_action, name='bulk_action'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:category_id>/edit/', views.category_update, name='category_update'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),

    # Units
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/<int:unit_id>/edit/', views.unit_update, name='unit_update'),
    path('units/<int:unit_id>/delete/', views.unit_delete, name='unit_delete'),
    
    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    
    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    
    # Stock Management
    path('stock-movements/', views.stock_movements, name='stock_movements'),
    path('alerts/', views.inventory_alerts, name='alerts'),
    path('low-stock/', views.low_stock_report, name='low_stock_report'),
    
    # Enhanced Alerts Management
    path('alerts/dashboard/', views.alerts_dashboard, name='alerts_dashboard'),
    path('alerts/list/', views.alerts_list, name='alerts_list'),
    path('alerts/<int:alert_id>/acknowledge/', views.acknowledge_alert, name='acknowledge_alert'),
    path('alerts/<int:alert_id>/resolve/', views.resolve_alert, name='resolve_alert'),
    path('alerts/bulk-acknowledge/', views.bulk_acknowledge_alerts, name='bulk_acknowledge_alerts'),
    path('alerts/refresh/', views.refresh_alerts, name='refresh_alerts'),
    path('purchase-requirements/', views.purchase_requirements, name='purchase_requirements'),

    # Settings Management
    path('settings/', views.settings_dashboard, name='settings_dashboard'),
    path('settings/shop/', views.shop_settings, name='shop_settings'),

    # Invoice Management
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
]