from django.urls import path ,include
from . import views

urlpatterns=[
    path('payment/list', views.paymentsList, name='payments'),
    path('payment/create', views.paymentCreate, name='paymentCreate'),
    path('payment/edit/<slug:slug>', views.paymentEdit, name='paymentEdit'),
    path('payment/delete/<slug:slug>', views.paymentDelete, name='paymentDelete'),

    path('expenses/list', views.expenseList, name='expenses'),
    path('expenses/create', views.expenseCreate, name='expense_create'),
    path('expenses/edit/<slug:slug>', views.expenseEdit, name='expense_edit'),
    path('expenses/delete/<slug:slug>', views.expenseDelete, name='expense_delete'),
]   