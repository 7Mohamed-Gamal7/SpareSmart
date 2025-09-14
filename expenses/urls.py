from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # Expenses
    path('', views.expense_list, name='expense_list'),
    path('create/', views.expense_create, name='expense_create'),
    path('<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('<int:expense_id>/edit/', views.expense_update, name='expense_update'),
    path('<int:expense_id>/approve/', views.expense_approve, name='expense_approve'),
    
    # Categories
    path('categories/', views.expense_category_list, name='expense_category_list'),
    path('categories/create/', views.expense_category_create, name='expense_category_create'),
    
    # Recurring Expenses
    path('recurring/', views.recurring_expense_list, name='recurring_expense_list'),
    path('recurring/create/', views.recurring_expense_create, name='recurring_expense_create'),
    
    # Petty Cash
    path('petty-cash/', views.petty_cash_list, name='petty_cash_list'),
    path('petty-cash/transaction/', views.petty_cash_transaction, name='petty_cash_transaction'),
]