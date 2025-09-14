from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def sale_list(request):
    return render(request, 'sales/sale_list.html', {'sales': []})

@login_required
def sale_create(request):
    messages.info(request, 'Sale creation feature coming soon!')
    return redirect('sales:sale_list')

@login_required
def sale_detail(request, sale_id):
    messages.info(request, 'Sale detail feature coming soon!')
    return redirect('sales:sale_list')

@login_required
def sale_update(request, sale_id):
    messages.info(request, 'Sale update feature coming soon!')
    return redirect('sales:sale_list')

@login_required
def sale_invoice(request, sale_id):
    messages.info(request, 'Invoice generation feature coming soon!')
    return redirect('sales:sale_list')

@login_required
def sale_print(request, sale_id):
    messages.info(request, 'Print feature coming soon!')
    return redirect('sales:sale_list')

@login_required
def payment_list(request, sale_id):
    messages.info(request, 'Payment management feature coming soon!')
    return redirect('sales:sale_list')

@login_required
def payment_create(request, sale_id):
    messages.info(request, 'Payment creation feature coming soon!')
    return redirect('sales:sale_list')

@login_required
def installment_list(request):
    return render(request, 'sales/installment_list.html', {'installments': []})

@login_required
def installment_detail(request, sale_id):
    messages.info(request, 'Installment detail feature coming soon!')
    return redirect('sales:installment_list')

@login_required
def installment_payment(request, installment_id):
    messages.info(request, 'Installment payment feature coming soon!')
    return redirect('sales:installment_list')