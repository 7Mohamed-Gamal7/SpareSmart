from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    # Purchases
    path('', views.purchase_list, name='purchase_list'),
    path('create/', views.purchase_create, name='purchase_create'),
    path('quick-purchase/', views.quick_purchase, name='quick_purchase'),
    path('<int:purchase_id>/', views.purchase_detail, name='purchase_detail'),
    path('<int:purchase_id>/edit/', views.purchase_update, name='purchase_update'),
    path('<int:purchase_id>/receive/', views.purchase_receive, name='purchase_receive'),
    path('<int:purchase_id>/invoice/', views.purchase_invoice, name='purchase_invoice'),
    
    # Payments
    path('<int:purchase_id>/payments/', views.purchase_payment_list, name='purchase_payment_list'),
    path('<int:purchase_id>/payments/add/', views.purchase_payment_create, name='purchase_payment_create'),
    
    # Returns
    path('returns/', views.purchase_return_list, name='purchase_return_list'),
    path('<int:purchase_id>/returns/create/', views.purchase_return_create, name='purchase_return_create'),
]