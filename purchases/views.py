from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def purchase_list(request):
    return render(request, 'purchases/purchase_list.html', {'purchases': []})

@login_required
def purchase_create(request):
    messages.info(request, 'Purchase creation feature coming soon!')
    return redirect('purchases:purchase_list')

@login_required
def purchase_detail(request, purchase_id):
    messages.info(request, 'Purchase detail feature coming soon!')
    return redirect('purchases:purchase_list')

@login_required
def purchase_update(request, purchase_id):
    messages.info(request, 'Purchase update feature coming soon!')
    return redirect('purchases:purchase_list')

@login_required
def purchase_receive(request, purchase_id):
    messages.info(request, 'Purchase receiving feature coming soon!')
    return redirect('purchases:purchase_list')

@login_required
def purchase_invoice(request, purchase_id):
    messages.info(request, 'Purchase invoice feature coming soon!')
    return redirect('purchases:purchase_list')

@login_required
def purchase_payment_list(request, purchase_id):
    messages.info(request, 'Purchase payment management feature coming soon!')
    return redirect('purchases:purchase_list')

@login_required
def purchase_payment_create(request, purchase_id):
    messages.info(request, 'Purchase payment creation feature coming soon!')
    return redirect('purchases:purchase_list')

@login_required
def purchase_return_list(request):
    return render(request, 'purchases/return_list.html', {'returns': []})

@login_required
def purchase_return_create(request, purchase_id):
    messages.info(request, 'Purchase return feature coming soon!')
    return redirect('purchases:purchase_return_list')