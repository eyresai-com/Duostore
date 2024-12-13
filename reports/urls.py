from django.urls import path
from .import views
from reports.views import *

urlpatterns = [
    # CRM Profit Loss Report
    path('admin/crm/reports/profit-loss-report/', views.profitLossReport, name='profitLossReport'),
    path('admin/crm/reports/this-year-profit-loss/print/', views.thisYearProfitLossPrint, name='thisYearProfitLossPrint'),
    path('admin/crm/reports/this-month-profit-loss/print/', views.thisMonthProfitLossPrint, name='thisMonthProfitLossPrint'),
    path('admin/crm/reports/previous-year-profit-loss/print/', views.previousYearProfitLossPrint, name='previousYearProfitLossPrint'),
    path('admin/crm/reports/all-time-profit-loss/print/', views.allTimeProfitLossPrint, name='allTimeProfitLossPrint'),
    
    # CRM Payments Report
    path('admin/crm/reports/payments-report/', views.paymentsReport, name='paymentsReport'),
    
    # CRM Expense Report
    path('admin/crm/reports/expenses-report/', views.expenseReport, name='expenseReport'),
    
        
    # CRM Invoice Report
    path('admin/crm/reports/invoice-report/', views.invoiceReport, name='invoiceReport'),
    path('admin/crm/reports/print/invoice/this-year', views.invoicePrintThisYear, name='invoicePrintThisYear'),
    path('admin/crm/reports/print/invoice/this-month', views.invoicePrintThisMonth, name='invoicePrintThisMonth'),
    path('admin/crm/reports/print/invoice/previous-year', views.invoicePrintPrevYear, name='invoicePrintPrevYear'),
    path('admin/crm/reports/print/invoice/all-time', views.invoicePrintAllTime, name='invoicePrintAllTime'),
    
    
    # CRM Orders Report
    path('admin/crm/reports/order-reports/', views.adminOrderReport, name='adminOrderReport'),
    path('admin/crm/reports/print/order/all-time', views.printAllTimeOrders, name='printAllTimeOrders'),
    path('admin/crm/reports/print/order/this-year', views.printThisYearOrders, name='printThisYearOrders'),
    path('admin/crm/reports/print/order/this-month', views.printThisMonthOrders, name='printThisMonthOrders'),
    path('admin/crm/reports/print/order/previous-year', views.printPrevYearOrders, name='printPrevYearOrders'),
    
    
    
   
  
    
]
