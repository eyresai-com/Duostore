from django.shortcuts import render
from django.utils import timezone
from django.contrib.admin.models import LogEntry
from products.models import *
from payments.models import *
from vendor.models import *
 
from invoice.models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required
from orders.models import *
from django.db.models import Count, Q, Sum
from decimal import Decimal

 
 
# Profit Loss Print
@login_required(login_url='login')
def thisYearProfitLossPrint(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # This year payment
    payments_for_current_year = Payment.objects.filter(payment_date__year=current_year, vendor=vendor)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    
    payments_for_current_month = Payment.objects.filter(payment_date__year=current_year, payment_date__month=current_month , vendor=vendor)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
 
    payments_for_previous_year = Payment.objects.filter(payment_date__year=previous_year , vendor=vendor)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    
    # This year expense
    expenses_for_current_year = Expense.objects.filter(date_of_expense__year=current_year , vendor=vendor)
    current_year_total_expense = expenses_for_current_year.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate the total discount_amount, tax_amount, and other_fees_amount for the current year
    invoices_for_current_year = Invoice.objects.filter(billDate__year=current_year , vendor=vendor) 
    current_year_total_other_fees = invoices_for_current_year.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0
    
    # This year calculation
    gross_profit_this_year = current_year_total_payment-current_year_total_expense
    net_profit_this_year = Decimal(gross_profit_this_year) - current_year_total_other_fees    
    context = {
        'title' : f'{current_year} Profit & Loss Report',
        'gross_profit_this_year' : gross_profit_this_year,
        'net_profit_this_year' : net_profit_this_year,
        'current_year_total_payment' : current_year_total_payment,
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment,
        'current_year_total_expense' : current_year_total_expense,

        'current_year_total_other_fees' : current_year_total_other_fees
    }
    return render(request, 'reports/thisYearProfitLossPrint.html', context)
 
@login_required(login_url='login')
def thisMonthProfitLossPrint(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Payments/Revenue Times
    payments_for_current_month = Payment.objects.filter(payment_date__year=current_year, payment_date__month=current_month , vendor=vendor)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
 
    payments_for_previous_year = Payment.objects.filter(payment_date__year=previous_year , vendor=vendor)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
 
    payments_for_current_year = Payment.objects.filter(payment_date__year=current_year , vendor=vendor)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    
    # Expense Times
    expenses_for_current_month = Expense.objects.filter(date_of_expense__year=current_year, date_of_expense__month=current_month , vendor=vendor) 
    current_month_total_expense = expenses_for_current_month.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate the total discount_amount, tax_amount, and other_fees_amount for the current month
    invoices_for_current_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month , vendor=vendor)
    current_month_total_other_fees = invoices_for_current_month.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0
    
    # This month calculation
    gross_profit_this_month = current_month_total_payment-current_month_total_expense
    net_profit_this_month = gross_profit_this_month - current_month_total_other_fees
    
    context = {
        'title' : f'{current_month}/{current_year} Profit & Loss Report',
        'gross_profit_this_month' : gross_profit_this_month,
        'net_profit_this_month' : net_profit_this_month,
        'current_year_total_payment' : current_year_total_payment,
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment,
        'current_month_total_expense' : current_month_total_expense,
 
        'current_month_total_other_fees' : current_month_total_other_fees
    }
    return render(request, 'reports/thisMonthProfitLossPrint.html', context)
 
@login_required(login_url='login')
def previousYearProfitLossPrint(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Payments/Revenue Times
    payments_for_current_month = Payment.objects.filter(payment_date__year=current_year, payment_date__month=current_month,vendor=vendor)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
 
    payments_for_previous_year = Payment.objects.filter(payment_date__year=previous_year,vendor=vendor)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
 
    payments_for_current_year = Payment.objects.filter(payment_date__year=current_year,vendor=vendor)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    
    # Expense Times
    expenses_for_previous_year = Expense.objects.filter(date_of_expense__year=previous_year,vendor=vendor)
    previous_year_total_expense = expenses_for_previous_year.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate the total discount_amount, tax_amount, and other_fees_amount for the previous year
    invoices_for_previous_year = Invoice.objects.filter(billDate__year=previous_year,vendor=vendor)
    previous_year_total_other_fees = invoices_for_previous_year.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0
    
    # previous year calculation
    gross_profit_previous_year = previous_year_total_payment-previous_year_total_expense
    net_profit_previous_year = gross_profit_previous_year-previous_year_total_other_fees
    
    context = {
        'title' : f'{previous_year} Profit & Loss Report',
        'gross_profit_previous_year' : gross_profit_previous_year,
        'net_profit_previous_year' : net_profit_previous_year,
        'current_year_total_payment' : current_year_total_payment,
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment,
        'previous_year_total_expense' : previous_year_total_expense,
 
        'previous_year_total_other_fees' : previous_year_total_other_fees
    }
    return render(request, 'reports/previousYearProfitLossPrint.html', context)
 
@login_required(login_url='login')
def allTimeProfitLossPrint(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
 
    # Payments/Revenue Times
    payments_for_current_month = Payment.objects.filter(payment_date__year=current_year, payment_date__month=current_month,vendor=vendor)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
 
    payments_for_previous_year = Payment.objects.filter(payment_date__year=previous_year,vendor=vendor)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
 
    payments_for_current_year = Payment.objects.filter(payment_date__year=current_year,vendor=vendor)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    
    # All time
    total_revenue = Payment.objects.aggregate(total_revenue=Sum('payment_amount'))
    total_revenue = total_revenue['total_revenue'] if total_revenue['total_revenue'] is not None else 0
    total_expense = Expense.objects.aggregate(total_expense=Sum('amount'))
    total_expense = total_expense['total_expense'] if total_expense['total_expense'] is not None else 0
    total_other_fees = Invoice.objects.aggregate(total_other_fees=Sum('other_fees_amount'))['total_other_fees'] or 0
    
    gross_profit = total_revenue-total_expense
    net_profit = gross_profit-total_other_fees
    
    context = {
        'title' : f'Profit & Loss Report',
        'gross_profit' : gross_profit,
        'net_profit' : net_profit,
        'total_revenue' : total_revenue,
        'total_expense' : total_expense,
 
        'total_other_fees' : total_other_fees,
        'current_year_total_payment' : current_year_total_payment,
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment
    }
    return render(request, 'reports/allTimeProfitLossPrint.html', context)
    
# Profit & Loss report
@login_required(login_url='login')
def profitLossReport(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')

    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1

    # Payments/Revenue
    payments_for_current_month = Payment.objects.filter(
        payment_date__year=current_year, payment_date__month=current_month, vendor=vendor
    )
    current_month_total_payment = Decimal(
        payments_for_current_month.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    )

    payments_for_current_year = Payment.objects.filter(
        payment_date__year=current_year, vendor=vendor
    )
    current_year_total_payment = Decimal(
        payments_for_current_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    )

    payments_for_previous_year = Payment.objects.filter(
        payment_date__year=previous_year, vendor=vendor
    )
    previous_year_total_payment = Decimal(
        payments_for_previous_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    )

    # Expenses
    expenses_for_current_year = Expense.objects.filter(date_of_expense__year=current_year, vendor=vendor)
    current_year_total_expense = Decimal(expenses_for_current_year.aggregate(Sum('amount'))['amount__sum'] or 0)

    expenses_for_current_month = Expense.objects.filter(
        date_of_expense__year=current_year, date_of_expense__month=current_month, vendor=vendor
    )
    current_month_total_expense = Decimal(expenses_for_current_month.aggregate(Sum('amount'))['amount__sum'] or 0)

    expenses_for_previous_year = Expense.objects.filter(date_of_expense__year=previous_year, vendor=vendor)
    previous_year_total_expense = Decimal(expenses_for_previous_year.aggregate(Sum('amount'))['amount__sum'] or 0)

    # Invoices and Fees
    invoices_for_current_year = Invoice.objects.filter(billDate__year=current_year, vendor=vendor)
    current_year_total_other_fees = Decimal(invoices_for_current_year.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0)

    invoices_for_current_month = Invoice.objects.filter(
        billDate__year=current_year, billDate__month=current_month, vendor=vendor
    )
    current_month_total_other_fees = Decimal(invoices_for_current_month.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0)

    invoices_for_previous_year = Invoice.objects.filter(billDate__year=previous_year, vendor=vendor)
    previous_year_total_other_fees = Decimal(invoices_for_previous_year.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0)

    # All-time Aggregates
    total_revenue = Decimal(Payment.objects.aggregate(total_revenue=Sum('payment_amount'))['total_revenue'] or 0)
    total_expense = Decimal(Expense.objects.aggregate(total_expense=Sum('amount'))['total_expense'] or 0)
    total_other_fees = Decimal(Invoice.objects.aggregate(total_other_fees=Sum('other_fees_amount'))['total_other_fees'] or 0)

    # Calculations
    gross_profit = total_revenue - total_expense
    net_profit = gross_profit - total_other_fees

    gross_profit_this_year = current_year_total_payment - current_year_total_expense
    net_profit_this_year = gross_profit_this_year - current_year_total_other_fees

    gross_profit_this_month = current_month_total_payment - current_month_total_expense
    net_profit_this_month = gross_profit_this_month - current_month_total_other_fees

    gross_profit_previous_year = previous_year_total_payment - previous_year_total_expense
    net_profit_previous_year = gross_profit_previous_year - previous_year_total_other_fees

    context = {
        'title': 'Profit/Loss Report',
        'current_year': current_year_total_payment,
        'current_month': current_month_total_payment,
        'previous_year': previous_year_total_payment,
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'total_other_fees': total_other_fees,
        'gross_profit': gross_profit,
        'net_profit': net_profit,
        'current_year_expense': current_year_total_expense,
        'current_month_expense': current_month_total_expense,
        'previous_year_expense': previous_year_total_expense,
        'current_year_other_fees_amount': current_year_total_other_fees,
        'current_month_other_fees_amount': current_month_total_other_fees,
        'previous_year_other_fees_amount': previous_year_total_other_fees,
        'gross_profit_this_year': gross_profit_this_year,
        'net_profit_this_year': net_profit_this_year,
        'gross_profit_this_month': gross_profit_this_month,
        'net_profit_this_month': net_profit_this_month,
        'gross_profit_previous_year': gross_profit_previous_year,
        'net_profit_previous_year': net_profit_previous_year,
    }

    return render(request, 'reports/profitLossReport.html', context)
 
# Payments report
@login_required(login_url='login')
def paymentsReport(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Payments/Revenue Times
    payments_for_current_month = Payment.objects.filter(payment_date__year=current_year, payment_date__month=current_month,vendor=vendor)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
 
    payments_for_previous_year = Payment.objects.filter(payment_date__year=previous_year,vendor=vendor)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
 
    payments_for_current_year = Payment.objects.filter(payment_date__year=current_year,vendor=vendor)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    
    # All time
    total_payments = Payment.objects.aggregate(total_revenue=Sum('payment_amount'))
    total_payments = total_payments['total_revenue'] if total_payments['total_revenue'] is not None else 0
    all_payments = Payment.objects.all()
    
    # Payments Table filter
    # Filter payments for the current year
    payments_this_year = Payment.objects.filter(payment_date__year=current_year,vendor=vendor)
 
    # Filter payments for the current month
    payments_this_month = Payment.objects.filter(payment_date__year=current_year, payment_date__month=current_month,vendor=vendor)
 
    # Filter payments for the previous year
    payments_previous_year = Payment.objects.filter(payment_date__year=previous_year,vendor=vendor)
 
    
    context = {
        'title' : 'Payments report',
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment,
        'current_year_total_payment' : current_year_total_payment,
        'total_payments' : total_payments,
        'payments_this_year': payments_this_year,
        'payments_this_month': payments_this_month,
        'payments_previous_year': payments_previous_year,
        'all_payments' : all_payments,
        'current_year' : current_year,
        'current_month' : current_month,
        'previous_year' : previous_year,
    }
    
    return render(request, 'reports/paymentsReport.html', context)
 
# Expense report
@login_required(login_url='login')
def expenseReport(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Expense Times
    expenses_for_current_year = Expense.objects.filter(date_of_expense__year=current_year,vendor=vendor)
    current_year_total_expense = expenses_for_current_year.aggregate(Sum('amount'))['amount__sum'] or 0
 
    expenses_for_current_month = Expense.objects.filter(date_of_expense__year=current_year, date_of_expense__month=current_month,vendor=vendor)
    current_month_total_expense = expenses_for_current_month.aggregate(Sum('amount'))['amount__sum'] or 0
 
    expenses_for_previous_year = Expense.objects.filter(date_of_expense__year=previous_year,vendor=vendor)
    previous_year_total_expense = expenses_for_previous_year.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Filter expenses for the current year
    expenses_this_year = Expense.objects.filter(date_of_expense__year=current_year,vendor=vendor)
 
    # Filter expenses for the current month
    expenses_this_month = Expense.objects.filter(date_of_expense__year=current_year, date_of_expense__month=current_month,vendor=vendor)
 
    # Filter expenses for the previous year
    expenses_previous_year = Expense.objects.filter(date_of_expense__year=previous_year,vendor=vendor)
    
    # All time
    total_expense = Expense.objects.aggregate(total_expense=Sum('amount'))
    total_expense = total_expense['total_expense'] if total_expense['total_expense'] is not None else 0
    all_time_expenses = Expense.objects.all()
    
    context = {
        'title' : 'Expense report',
        'current_month_total_expense' : current_month_total_expense,
        'previous_year_total_expense' : previous_year_total_expense,
        'current_year_total_expense' : current_year_total_expense,
        'expenses_this_year': expenses_this_year,
        'expenses_this_month': expenses_this_month,
        'expenses_previous_year': expenses_previous_year,
        'total_expense' : total_expense,
        'all_time_expenses_table' : all_time_expenses,
        'current_year' : current_year,
        'current_month' : current_month,
        'previous_year' : previous_year,
    }
    
    return render(request, 'reports/expenseReport.html', context)
 
 
 
# CRM Invoice This Year Print
@login_required(login_url='login')
def invoicePrintThisYear(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year,vendor=vendor)
 
    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month,vendor=vendor)
 
    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year,vendor=vendor)
 
    # Get the counts of invoices in different statuses
    total_invoices_this_year = invoices_this_year.count()
    total_paid_this_year = invoices_this_year.filter(status='PAID').count()
    total_unpaid_this_year = invoices_this_year.filter(status='UNPAID').count()
    total_overdue_this_year = invoices_this_year.filter(status='OVERDUE').count()
    
    total_invoices_this_month = invoices_this_month.count()
    total_invoices_previous_year = invoices_previous_year.count()
    
    context = {
        'title' : f'{current_year} Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_this_year': total_invoices_this_year,
        'total_paid_this_year': total_paid_this_year,
        'total_unpaid_this_year': total_unpaid_this_year,
        'total_overdue_this_year': total_overdue_this_year,
        'total_invoices_this_month' : total_invoices_this_month,
        'total_invoices_previous_year' : total_invoices_previous_year,
        
    }
    return render(request, 'reports/invoicePrintThisYear.html', context)
 
# CRM Invoice This Month Print
@login_required(login_url='login')
def invoicePrintThisMonth(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year,vendor=vendor)
 
    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month,vendor=vendor)
 
    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year,vendor=vendor)
    
    total_invoices_this_month = invoices_this_month.count()
    total_paid_this_month = invoices_this_month.filter(status='PAID').count()
    total_unpaid_this_month = invoices_this_month.filter(status='UNPAID').count()
    total_overdue_this_month = invoices_this_month.filter(status='OVERDUE').count()
 
    total_invoices_this_year = invoices_this_year.count()
    total_invoices_previous_year = invoices_previous_year.count()
    
    context = {
        'title' : f'{current_month}/{current_year} Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_this_month' : total_invoices_this_month,
        'total_paid_this_month' : total_paid_this_month,
        'total_unpaid_this_month' : total_unpaid_this_month,
        'total_overdue_this_month' : total_overdue_this_month,
        'total_invoices_this_year' : total_invoices_this_year,
        'total_invoices_previous_year' : total_invoices_previous_year
    }
    return render(request, 'reports/invoicePrintThisMonth.html', context)
 
# CRM Invoice Previous Year Print
@login_required(login_url='login')
def invoicePrintPrevYear(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year,vendor=vendor)
 
    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month,vendor=vendor)
 
    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year,vendor=vendor)
    
    # Previous Year
    total_invoices_previous_year = invoices_previous_year.count()
    total_paid_previous_year = invoices_previous_year.filter(status='PAID').count()
    total_unpaid_previous_year = invoices_previous_year.filter(status='UNPAID').count()
    total_overdue_previous_year = invoices_previous_year.filter(status='OVERDUE').count()
    
    total_invoices_this_year = invoices_this_year.count()
    total_invoices_this_month = invoices_this_month.count()
    
    context = {
        'title' : f'{previous_year} Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_previous_year' : total_invoices_previous_year,
        'total_paid_previous_year' : total_paid_previous_year,
        'total_unpaid_previous_year' : total_unpaid_previous_year,
        'total_overdue_previous_year' : total_overdue_previous_year,
        'total_invoices_this_year' : total_invoices_this_year,
        'total_invoices_this_month' : total_invoices_this_month
    }
    
    return render(request, 'reports/invoicePrintPrevYear.html', context)
 
# CRM Invoice All Time Print
@login_required(login_url='login')
def invoicePrintAllTime(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year,vendor=vendor)
 
    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month,vendor=vendor)
 
    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year,vendor=vendor)
    
    total_invoices_this_year = invoices_this_year.count()
    total_invoices_this_month = invoices_this_month.count()
    total_invoices_previous_year = invoices_previous_year.count()
    
    # All Time
    total_invoices = Invoice.objects.all().count()
    total_paid_invoices = Invoice.objects.filter(status="PAID").count()
    total_unpaid_invoices = Invoice.objects.filter(status="UNPAID").count()
    total_overdue_invoices = Invoice.objects.filter(status="OVERDUE").count()
    
    context = {
        'title' : 'Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices' : total_invoices,
        'total_paid_invoices' : total_paid_invoices,
        'total_unpaid_invoices' : total_unpaid_invoices,
        'total_overdue_invoices' : total_overdue_invoices,
        
        'total_invoices_this_year' : total_invoices_this_year,
        'total_invoices_this_month' : total_invoices_this_month,
        'total_invoices_previous_year' : total_invoices_previous_year
        
    }
    return render(request, 'reports/invoicePrintAllTime.html', context)
    
# CRM Invoice reports
@login_required(login_url='login')
 
def invoiceReport(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
 
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year,vendor=vendor)
 
    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(
        billDate__year=current_year, 
        billDate__month=current_month, 
        vendor=vendor
    ) 
        # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year,vendor=vendor)
 
    # This Year
    total_invoices_this_year = invoices_this_year.count()
    total_paid_this_year = invoices_this_year.filter(status='PAID').count()
    total_unpaid_this_year = invoices_this_year.filter(status='UNPAID').count()
    total_overdue_this_year = invoices_this_year.filter(status='OVERDUE').count()
 
    # This Month
    total_invoices_this_month = invoices_this_month.count()
    total_paid_this_month = invoices_this_month.filter(status='PAID').count()
    total_unpaid_this_month = invoices_this_month.filter(status='UNPAID').count()
    total_overdue_this_month = invoices_this_month.filter(status='OVERDUE').count()
 
    # Previous Year
    total_invoices_previous_year = invoices_previous_year.count()
    total_paid_previous_year = invoices_previous_year.filter(status='PAID').count()
    total_unpaid_previous_year = invoices_previous_year.filter(status='UNPAID').count()
    total_overdue_previous_year = invoices_previous_year.filter(status='OVERDUE').count()
    
    # All Time
    total_invoices = Invoice.objects.all()
    total_count = total_invoices.count()
    total_paid_invoices = Invoice.objects.filter(status="PAID").count()
    total_unpaid_invoices = Invoice.objects.filter(status="UNPAID").count()
    total_overdue_invoices = Invoice.objects.filter(status="OVERDUE").count()
 
    context = {
        'title': 'Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'total_invoices' : total_invoices,
        'total_count' : total_count,
        'total_paid_invoices' : total_paid_invoices,
        'total_unpaid_invoices' : total_unpaid_invoices,
        'total_overdue_invoices' : total_overdue_invoices,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_this_year': total_invoices_this_year,
        'total_paid_this_year': total_paid_this_year,
        'total_unpaid_this_year': total_unpaid_this_year,
        'total_overdue_this_year': total_overdue_this_year,
        
        'total_invoices_this_month': total_invoices_this_month,
        'total_paid_this_month': total_paid_this_month,
        'total_unpaid_this_month': total_unpaid_this_month,
        'total_overdue_this_month': total_overdue_this_month,
        
        'total_invoices_previous_year': total_invoices_previous_year,
        'total_paid_previous_year': total_paid_previous_year,
        'total_unpaid_previous_year': total_unpaid_previous_year,
        'total_overdue_previous_year': total_overdue_previous_year,
    }
 
    return render(request, 'reports/invoiceReport.html', context)
 
 
# Order Report
@login_required(login_url='login')
 
def adminOrderReport(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    orders = Order.objects.filter(is_ordered=True)
    total_value = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    order_pending = Order.objects.filter(status='pending', is_ordered=True)
    order_confirmed = Order.objects.filter(status='confirmed', is_ordered=True)
    order_completed = Order.objects.filter(status='completed', is_ordered=True)
    order_canceled = Order.objects.filter(status='canceled', is_ordered=True)
    
    # Order this month
    order_this_month = Order.objects.filter(ordered_at__year=current_year, ordered_at__month=current_month, is_ordered=True,vendor=vendor)
    total_value_this_month = order_this_month.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_this_month = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    confirmed_order_this_month = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    completed_order_this_month = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    canceled_order_this_month = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    
    # Order this year
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year)
    total_value_this_year = order_this_year.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_this_year = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=current_year,vendor=vendor)
    confirmed_order_this_year = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=current_year,vendor=vendor)
    completed_order_this_year = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=current_year,vendor=vendor)
    canceled_order_this_year = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=current_year,vendor=vendor)
    
    # Order previous year
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year)
    total_value_previous_year = order_previous_year.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_previous_year = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=previous_year,vendor=vendor)
    confirmed_order_previous_year = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=previous_year,vendor=vendor)
    completed_order_previous_year = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=previous_year,vendor=vendor)
    canceled_order_previous_year = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=previous_year,vendor=vendor)
 
    context = {
        'title' : 'Order Reports',
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'orders' : orders,
        'total_value':total_value,
        'order_pending' : order_pending,
        'order_confirmed' : order_confirmed,
        'order_completed' : order_completed,
        'order_canceled' : order_canceled,
        
        'order_this_month' : order_this_month,
        'total_value_this_month' : total_value_this_month,
        'pending_order_this_month' : pending_order_this_month,
        'confirmed_order_this_month' : confirmed_order_this_month,
        'completed_order_this_month' : completed_order_this_month,
        'canceled_order_this_month' : canceled_order_this_month,
        
        'order_this_year' : order_this_year,
        'total_value_this_year' : total_value_this_year,
        'pending_order_this_year' : pending_order_this_year,
        'confirmed_order_this_year' : confirmed_order_this_year,
        'completed_order_this_year' : completed_order_this_year,
        'canceled_order_this_year' : canceled_order_this_year,
        
        'order_previous_year' : order_previous_year,
        'total_value_previous_year' : total_value_previous_year,
        'pending_order_previous_year' : pending_order_previous_year,
        'confirmed_order_previous_year': confirmed_order_previous_year,
        'completed_order_previous_year' : completed_order_previous_year,
        'canceled_order_previous_year' : canceled_order_previous_year,
    }
    
    return render(request, 'reports/adminOrderReport.html', context)
 
# Print This Year Orders
@login_required(login_url='login')
def printThisYearOrders(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year,vendor=vendor)
    total_value_this_year = order_this_year.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_this_year = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=current_year,vendor=vendor)
    confirmed_order_this_year = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=current_year,vendor=vendor)
    completed_order_this_year = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=current_year,vendor=vendor)
    canceled_order_this_year = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=current_year,vendor=vendor)
    
    order_this_month = Order.objects.filter(is_ordered=True, ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year,vendor=vendor)
    
    context = {
        'title' : f'{current_year} Order Report',
        
        'order_this_year' : order_this_year,
        'total_value_this_year' : total_value_this_year,
        'pending_order_this_year' : pending_order_this_year,
        'confirmed_order_this_year' : confirmed_order_this_year,
        'completed_order_this_year' : completed_order_this_year,
        'canceled_order_this_year' : canceled_order_this_year,
        
        'order_this_month' : order_this_month,
        'order_previous_year' : order_previous_year,
    }
    
    return render(request, 'reports/printThisYearOrders.html', context)
 
# Print This Month Orders
@login_required(login_url='login')
def printThisMonthOrders(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    order_this_month = Order.objects.filter(is_ordered=True, ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    total_value_this_month = order_this_month.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_this_month = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    confirmed_order_this_month = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    completed_order_this_month = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    canceled_order_this_month = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year)
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year)
    
    context = {
        'title' : f'{current_month}/{current_year} Order Report',
        
        'order_this_month' : order_this_month,
        'total_value_this_month' : total_value_this_month,
        'pending_order_this_month' : pending_order_this_month,
        'confirmed_order_this_month' : confirmed_order_this_month,
        'completed_order_this_month' : completed_order_this_month,
        'canceled_order_this_month' : canceled_order_this_month,
        
        'order_this_year' : order_this_year,
        'order_previous_year' : order_previous_year,
    }
    
    return render(request, 'reports/printThisMonthOrders.html', context)
 
# Print Previous Year Orders
@login_required(login_url='login')
def printPrevYearOrders(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year,vendor=vendor)
    total_value_previous_year = order_previous_year.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_previous_year = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=previous_year,vendor=vendor)
    confirmed_order_previous_year = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=previous_year,vendor=vendor)
    completed_order_previous_year = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=previous_year,vendor=vendor)
    canceled_order_previous_year = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=previous_year,vendor=vendor)
    
    order_this_month = Order.objects.filter(is_ordered=True, ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year,vendor=vendor)
    
    
    context = {
        'title' : f'{previous_year} Order Report',
        
        'order_previous_year' : order_previous_year,
        'total_value_previous_year' : total_value_previous_year,
        'pending_order_previous_year' : pending_order_previous_year,
        'confirmed_order_previous_year': confirmed_order_previous_year,
        'completed_order_previous_year' : completed_order_previous_year,
        'canceled_order_previous_year' : canceled_order_previous_year,
        
        'order_this_month' : order_this_month,
        'order_this_year' : order_this_year,
        
    }
    
    return render(request, 'reports/printPrevYearOrders.html', context)
 
# Print All Time Orders
@login_required(login_url='login')
def printAllTimeOrders(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('login')
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    orders = Order.objects.filter(is_ordered=True)
    total_value = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    order_pending = Order.objects.filter(is_ordered=True, status='pending')
    order_confirmed = Order.objects.filter(is_ordered=True, status='confirmed')
    order_completed = Order.objects.filter(is_ordered=True, status='completed')
    order_canceled = Order.objects.filter(is_ordered=True, status='canceled')
    
    order_this_month = Order.objects.filter(is_ordered=True, ordered_at__year=current_year, ordered_at__month=current_month,vendor=vendor)
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year,vendor=vendor)
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year,vendor=vendor)
    
    context = {
        'title' : 'Order Report',
        
        'orders' : orders,
        'total_value':total_value,
        'order_pending' : order_pending,
        'order_confirmed' : order_confirmed,
        'order_completed' : order_completed,
        'order_canceled' : order_canceled,
        
        'order_this_month' : order_this_month,
        'order_this_year' : order_this_year,
        'order_previous_year' : order_previous_year,
    }
    
    return render(request, 'reports/printAllTimeOrders.html', context)
 
# Activity log report
@login_required(login_url='login')
def activityLogReport(request):
    
    recent_actions = LogEntry.objects.all().order_by('-action_time')
    
    context = {
        'title' : 'Activity Logs',
        'recent_actions' : recent_actions,
    }
 
    return render(request, 'reports/activityLogReport.html', context)
 
 
 
# ====================Error Page====================
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)
 
def error_500(request):
    return render(request, 'error/error_500.html', status=500)