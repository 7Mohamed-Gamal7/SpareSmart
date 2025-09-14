from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def reports_home(request):
    return render(request, 'reports/home.html', {})

@login_required
def generate_report(request):
    messages.info(request, 'Report generation feature coming soon!')
    return redirect('reports:reports_home')

@login_required
def report_template_list(request):
    return render(request, 'reports/template_list.html', {'templates': []})

@login_required
def report_template_create(request):
    messages.info(request, 'Report template creation feature coming soon!')
    return redirect('reports:report_template_list')

@login_required
def report_template_detail(request, template_id):
    messages.info(request, 'Report template detail feature coming soon!')
    return redirect('reports:report_template_list')

@login_required
def generated_report_list(request):
    return render(request, 'reports/generated_list.html', {'reports': []})

@login_required
def generated_report_detail(request, report_id):
    messages.info(request, 'Generated report detail feature coming soon!')
    return redirect('reports:generated_report_list')

@login_required
def download_report(request, report_id):
    messages.info(request, 'Report download feature coming soon!')
    return redirect('reports:generated_report_list')

@login_required
def sales_report(request):
    messages.info(request, 'Sales report feature coming soon!')
    return redirect('reports:reports_home')

@login_required
def purchases_report(request):
    messages.info(request, 'Purchases report feature coming soon!')
    return redirect('reports:reports_home')

@login_required
def inventory_report(request):
    messages.info(request, 'Inventory report feature coming soon!')
    return redirect('reports:reports_home')

@login_required
def expenses_report(request):
    messages.info(request, 'Expenses report feature coming soon!')
    return redirect('reports:reports_home')

@login_required
def profit_loss_report(request):
    messages.info(request, 'Profit & Loss report feature coming soon!')
    return redirect('reports:reports_home')

@login_required
def installments_report(request):
    messages.info(request, 'Installments report feature coming soon!')
    return redirect('reports:reports_home')