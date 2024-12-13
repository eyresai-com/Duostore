from django.urls import path , include
from . import views

urlpatterns=[
    path('vendorDashboard', views.vendorDashboard, name="vendorDashboard"),
    path('v_profile', views.v_profile, name="v_profile"),
    
    
    
    
]