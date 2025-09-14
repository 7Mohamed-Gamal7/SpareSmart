from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Reports Dashboard
    path('', views.reports_home, name='reports_home'),
    
    # Report Generation
    path('generate/', views.generate_report, name='generate_report'),
    path('templates/', views.report_template_list, name='report_template_list'),
    path('templates/create/', views.report_template_create, name='report_template_create'),
    path('templates/<int:template_id>/', views.report_template_detail, name='report_template_detail'),
    
    # Generated Reports
    path('generated/', views.generated_report_list, name='generated_report_list'),
    path('generated/<int:report_id>/', views.generated_report_detail, name='generated_report_detail'),
    path('generated/<int:report_id>/download/', views.download_report, name='download_report'),
    
    # Predefined Reports
    path('sales/', views.sales_report, name='sales_report'),
    path('purchases/', views.purchases_report, name='purchases_report'),
    path('inventory/', views.inventory_report, name='inventory_report'),
    path('expenses/', views.expenses_report, name='expenses_report'),
    path('profit-loss/', views.profit_loss_report, name='profit_loss_report'),
    path('installments/', views.installments_report, name='installments_report'),
]