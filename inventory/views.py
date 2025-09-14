from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

@login_required
def product_list(request):
    return render(request, 'inventory/product_list.html', {'products': []})

@login_required
def product_create(request):
    messages.info(request, 'Product creation feature coming soon!')
    return redirect('inventory:product_list')

@login_required
def product_detail(request, product_id):
    messages.info(request, 'Product detail feature coming soon!')
    return redirect('inventory:product_list')

@login_required
def product_update(request, product_id):
    messages.info(request, 'Product update feature coming soon!')
    return redirect('inventory:product_list')

@login_required
def category_list(request):
    messages.info(request, 'Category management coming soon!')
    return redirect('inventory:product_list')

@login_required
def category_create(request):
    messages.info(request, 'Category creation coming soon!')
    return redirect('inventory:product_list')

@login_required
def customer_list(request):
    return render(request, 'inventory/customer_list.html', {'customers': []})

@login_required
def customer_create(request):
    messages.info(request, 'Customer creation feature coming soon!')
    return redirect('inventory:customer_list')

@login_required
def customer_detail(request, customer_id):
    messages.info(request, 'Customer detail feature coming soon!')
    return redirect('inventory:customer_list')

@login_required
def supplier_list(request):
    return render(request, 'inventory/supplier_list.html', {'suppliers': []})

@login_required
def supplier_create(request):
    messages.info(request, 'Supplier creation feature coming soon!')
    return redirect('inventory:supplier_list')

@login_required
def supplier_detail(request, supplier_id):
    messages.info(request, 'Supplier detail feature coming soon!')
    return redirect('inventory:supplier_list')

@login_required
def stock_movements(request):
    messages.info(request, 'Stock movements feature coming soon!')
    return redirect('inventory:product_list')

@login_required
def inventory_alerts(request):
    messages.info(request, 'Inventory alerts feature coming soon!')
    return redirect('inventory:product_list')

@login_required
def low_stock_report(request):
    messages.info(request, 'Low stock report feature coming soon!')
    return redirect('inventory:product_list')