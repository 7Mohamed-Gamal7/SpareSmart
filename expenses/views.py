from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def expense_list(request):
    return render(request, 'expenses/expense_list.html', {'expenses': []})

@login_required
def expense_create(request):
    messages.info(request, 'Expense creation feature coming soon!')
    return redirect('expenses:expense_list')

@login_required
def expense_detail(request, expense_id):
    messages.info(request, 'Expense detail feature coming soon!')
    return redirect('expenses:expense_list')

@login_required
def expense_update(request, expense_id):
    messages.info(request, 'Expense update feature coming soon!')
    return redirect('expenses:expense_list')

@login_required
def expense_approve(request, expense_id):
    messages.info(request, 'Expense approval feature coming soon!')
    return redirect('expenses:expense_list')

@login_required
def expense_category_list(request):
    messages.info(request, 'Expense category management feature coming soon!')
    return redirect('expenses:expense_list')

@login_required
def expense_category_create(request):
    messages.info(request, 'Expense category creation feature coming soon!')
    return redirect('expenses:expense_list')

@login_required
def recurring_expense_list(request):
    return render(request, 'expenses/recurring_list.html', {'recurring_expenses': []})

@login_required
def recurring_expense_create(request):
    messages.info(request, 'Recurring expense feature coming soon!')
    return redirect('expenses:recurring_expense_list')

@login_required
def petty_cash_list(request):
    return render(request, 'expenses/petty_cash_list.html', {'transactions': []})

@login_required
def petty_cash_transaction(request):
    messages.info(request, 'Petty cash management feature coming soon!')
    return redirect('expenses:petty_cash_list')