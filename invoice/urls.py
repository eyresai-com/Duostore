from django.urls import path ,include
from . import views

urlpatterns=[

    path('invoices/', views.invoiceList, name='InvoiceList'),
    path('invoices/create', views.createInvoice, name='crmInvoiceCreate'),
    
    path('invoices/build/<slug:slug>',views.createBuildInvoice, name='create-build-invoice'),
    path('invoices/delete/<slug:slug>', views.deleteInvoice, name='deleteInvoice'),
    path('invoice/view/<slug:slug>', views.viewPrintnvoice, name='viewPrintnvoice'),


    path('invoices/<slug:slug>/delete/product/<int:product_id>/', views.delete_invoice_product, name='delete-invoice-product'),

  
]   