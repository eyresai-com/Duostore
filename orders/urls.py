from django.urls import path
from .import views
from .views import *
from orders.vendor_dash import *

urlpatterns = [
    path('list', views.adminAllOrders, name='adminAllOrders'),
    path('pending-orders', views.adminPendingOrders, name='adminPendingOrders'),
    path('confirmed-orders', views.adminConfirmedOrders, name='adminConfirmedOrders'),
    path('completed-orders', views.adminCompletedOrders, name='adminCompletedOrders'),
    path('canceled-orders', views.adminCanceledOrders, name='adminCanceledOrders'),
    
    # Order Details
    path('<int:user>/<str:order_id>', adminOrderDetails, name='adminOrderDetails'),
    
    # Order Delete
    path('delete/<str:order_id>', adminOrderDelete, name='adminOrderDelete'),
]