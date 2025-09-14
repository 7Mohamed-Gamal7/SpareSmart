from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Sales
    path('', views.sale_list, name='sale_list'),
    path('create/', views.sale_create, name='sale_create'),
    path('<int:sale_id>/', views.sale_detail, name='sale_detail'),
    path('<int:sale_id>/edit/', views.sale_update, name='sale_update'),
    path('<int:sale_id>/invoice/', views.sale_invoice, name='sale_invoice'),
    path('<int:sale_id>/print/', views.sale_print, name='sale_print'),
    
    # Payments
    path('<int:sale_id>/payments/', views.payment_list, name='payment_list'),
    path('<int:sale_id>/payments/add/', views.payment_create, name='payment_create'),
    
    # Installments
    path('installments/', views.installment_list, name='installment_list'),
    path('<int:sale_id>/installments/', views.installment_detail, name='installment_detail'),
    path('installments/<int:installment_id>/payment/', views.installment_payment, name='installment_payment'),
]