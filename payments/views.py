from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

#------------------------------------------ Payments -------------------------#

# Create your views here.
@login_required(login_url='login')

def paymentsList(request):
    payments = Payment.objects.all()
    
    context = {
        'title': 'Payments',
        'payments': payments,
    }
    return render(request, 'payments/payments.html', context)


@login_required(login_url='login')
def paymentCreate(request):
    try:
        vendor = Vendor.objects.get(user=request.user)  # Ensure vendor exists for the user
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not associated with a vendor account.')
        return redirect('payments')

    if request.method == 'POST':
        form = PaymentsForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.vendor = vendor  # Assign the vendor instance
            payment.save()
            messages.success(request, 'Payment created successfully!')
            return redirect('payments')
    else:
        form = PaymentsForm()

    context = {
        'title': 'Create Payment',
        'form': form,
    }
    return render(request, 'payments/create.html', context)

@login_required(login_url='login')
def paymentEdit(request, slug):
    # Retrieve the vendor associated with the logged-in user
    try:
        vendor = Vendor.objects.get(user=request.user)  # Ensure vendor exists for the user
        payment = get_object_or_404(Payment, slug=slug, vendor=vendor)  # Ensure the payment belongs to the vendor
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not associated with a vendor account.')
        return redirect('payments')

    if request.method == 'POST':
        form = PaymentsForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()  # Save the updated payment
            messages.success(request, 'Payment updated successfully!')
            return redirect('payments')
    else:
        form = PaymentsForm(instance=payment)  # Populate form with existing payment data

    context = {
        'title': 'Edit Payment',
        'form': form,
        'payment': payment,
    }
    return render(request, 'payments/edit.html', context)

@login_required(login_url='login')
def paymentDelete(request, slug):
    payment = get_object_or_404(Payment, slug=slug)
    payment.delete()
    messages.warning(request, 'Payment deleted successfully!')
    return redirect('payments')



#------------------------------- Expenses --------------------------------------#


@login_required(login_url='login')
def expenseList(request):
    # Retrieve expenses associated with the logged-in user's vendor
    try:
        vendor = Vendor.objects.get(user=request.user)
        expenses = Expense.objects.filter(vendor=vendor)  # Filter expenses by vendor
    except Vendor.DoesNotExist:
        expenses = []

    context = {
        'title': 'Expenses',
        'expenses': expenses,
    }
    return render(request, 'expenses/expenses.html', context)

@login_required(login_url='login')
def expenseCreate(request):
    try:
        vendor = Vendor.objects.get(user=request.user)  # Ensure vendor exists for the user
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not associated with a vendor account.')
        return redirect('expenses')

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.vendor = vendor  # Assign the vendor instance
            expense.save()
            messages.success(request, 'Expense created successfully!')
            return redirect('expenses')
    else:
        form = ExpenseForm()

    context = {
        'title': 'Create Expense',
        'form': form,
    }
    return render(request, 'expenses/create.html', context)

@login_required(login_url='login')
def expenseEdit(request, slug):
    # Retrieve the vendor associated with the logged-in user
    try:
        vendor = Vendor.objects.get(user=request.user)
        expense = get_object_or_404(Expense, slug=slug, vendor=vendor)  # Ensure the expense belongs to the vendor
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not associated with a vendor account.')
        return redirect('expenses')

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()  # Save the updated expense
            messages.success(request, 'Expense updated successfully!')
            return redirect('expenses')
    else:
        form = ExpenseForm(instance=expense)  # Populate form with existing expense data

    context = {
        'title': 'Edit Expense',
        'form': form,
        'expense': expense,
    }
    return render(request, 'expenses/edit.html', context)

@login_required(login_url='login')
def expenseDelete(request, slug):
    try:
        vendor = Vendor.objects.get(user=request.user)  # Ensure vendor exists for the user
        expense = get_object_or_404(Expense, slug=slug, vendor=vendor)  # Ensure the expense belongs to the vendor
        expense.delete()
        messages.warning(request, 'Expense deleted successfully!')
        return redirect('expenses')
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not associated with a vendor account.')
        return redirect('expenses')