from django.shortcuts import render, get_object_or_404, redirect
from accounts.views import *
from accounts.models import *
from .models import *
from .forms import *
from invoice.models import *
from payments.models import *
from django.db.models import Sum
from django.db.models.functions import TruncMonth



def vendorDashboard(request):
    # Get the vendor associated with the logged-in user
    vendor = get_object_or_404(Vendor, user=request.user)

    # Calculate total revenue for this vendor
    total_revenue = Payment.objects.filter(vendor=vendor).aggregate(total_revenue=Sum('payment_amount'))
    total_revenue = total_revenue['total_revenue'] if total_revenue['total_revenue'] is not None else 0

    # Calculate total expense for this vendor
    total_expense = Expense.objects.filter(vendor=vendor).aggregate(total_expense=Sum('amount'))
    total_expense = total_expense['total_expense'] if total_expense['total_expense'] is not None else 0

    # Calculate profit or loss
    profit = total_revenue - total_expense
    result = "Profitable" if profit >= 0 else "Loss"

    # Filter invoices, payments, and expenses for this vendor
    invoices = Invoice.objects.filter(vendor=vendor)
    paid_count = invoices.filter(status='PAID').count()
    unpaid_count = invoices.exclude(status='PAID').count()
    overdue_count = invoices.filter(status='OVERDUE').count()
    
    payments = Payment.objects.filter(vendor=vendor).order_by('-payment_date')
    expenses = Expense.objects.filter(vendor=vendor).order_by('-date_of_expense')

    monthly_revenue = (
        Payment.objects.filter(vendor=vendor)
        .annotate(month=TruncMonth('payment_date'))
        .values('month')
        .annotate(total=Sum('payment_amount'))
        .order_by('month')
    )

    # Calculate monthly expense for the current year
    monthly_expense = (
        Expense.objects.filter(vendor=vendor)
        .annotate(month=TruncMonth('date_of_expense'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Prepare data for the chart
    chart_data = {
        'months': [entry['month'].strftime('%B') for entry in monthly_revenue],
        'revenues': [{'month': entry['month'].strftime('%B'), 'revenue': entry['total']} for entry in monthly_revenue],
        'expenses': [entry['total'] for entry in monthly_expense],
        'profits': [revenue - expense for revenue, expense in zip(
            [entry['total'] for entry in monthly_revenue],
            [entry['total'] for entry in monthly_expense]
        )]
    }



    context = {
        'title': 'CRM',
        'payments': payments,
        'expenses': expenses,
        
        # Revenue Expense Chart
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'profit': profit,
        'result': result,
        
        # Invoice Chart
        'invoice': invoices,
        'paid_invoice': paid_count,
        'unpaid_invoice': unpaid_count,
        'overdue_invoice': overdue_count,
        'chart_data': chart_data,
    }
    return render(request, 'vendor/vendordashboard.html', context)







@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def v_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile updated.')
            return redirect('v_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance = vendor)    


    context = {
        'profile_form' : profile_form,
        'vendor_form' : vendor_form,
        'profile' : profile,
        'vendor' : vendor,
    }

    

    return render(request,'vendor/v_profile.html', context)
