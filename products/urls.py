from django.urls import path , include
from . import views

urlpatterns=[
    path('add_product',views.add_product,name='add_product'),
    path('product_items',views.product_items,name='product_items'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),


    
    
    path('add_category',views.add_category,name='add_category'),
    path('category_items',views.category_items,name='category_items'),
    path('edit_category/<int:category_id>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),


    
    
    path('add_brand',views.add_brand,name='add_brand'),
    path('brand_items',views.brand_items,name='brand_items'),
    path('edit_brand/<int:brand_id>/',views.edit_brand,name='edit_brand'),
    path('delete_brand/<int:brand_id>/',views.delete_brand,name='delete_brand'),






]
  
    
    