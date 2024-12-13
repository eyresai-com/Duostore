from django.urls import path , include
from . import views

urlpatterns=[

    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('overview/' , views.overview, name="overview"),
    path('prods/' , views.prods, name="prods"),
    path('prods/<slug:vendor_slug>/', views.prods_detail, name='prods_detail'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),





    path('post_list/' , views.post_list, name="post_list"),
	path('post_detail/<int:id>/', views.post_detail, name='post_detail'),
	path('post_list/tags=<slug:tag>/', views.post_by_tag, name='post_by_tag'),
	path('post_list/category=<slug:category>', views.post_by_category, name='post_by_category'),

    path('contact/' , views.contact, name="contact"),





]