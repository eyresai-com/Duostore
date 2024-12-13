from django.urls import path , include
from . import views

urlpatterns=[



    path('accounts/registerUser', views.registerUser, name="registerUser"),
    path('accounts/registerVendor', views.registerVendor, name="registerVendor"),




    path('accounts/activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('accounts/login/', views.login, name='login'),
    path('accounts/forgot_password/', views.forgot_password, name='forgot_password'),
    path('accounts/reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('accounts/reset_password/', views.reset_password, name='reset_password'),



    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/myAccount/', views.myAccount, name='myAccount'),
    path('accounts/product/', include('products.urls')),
    path('accounts/invoice/', include('invoice.urls')),
    path('accounts/', include('payments.urls')),
    path('accounts/orders/', include('orders.urls')),
    path('accounts/report/', include('reports.urls')),











    path('vendor/', include('vendor.urls')),




]