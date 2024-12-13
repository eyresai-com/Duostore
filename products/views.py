from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required , user_passes_test
from accounts.views import *
from .forms import *
from .views import *


from django.contrib import messages 

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_product(request):
  
    if request.method == 'POST':
        form = Product_Form(request.POST,request.FILES)
        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.vendor = Vendor.objects.get(user=request.user)
            product_instance.save()
            messages.success(request, f'{Product.product_name} created successfully')
            return redirect('product_items')
    else:
        form = Product_Form()        
    context = {
        'title': 'Add new product',
        'Product_Form' : form

    }
    return render(request,'products/add_product.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_items(request):
    vendor = Vendor.objects.filter(user=request.user)
    product = Product.objects.filter(vendor__in=vendor)
    context = {
        'product': product
    }
    
    return render(request, 'products/product.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_product(request,product_id):
    product_instance = get_object_or_404(Product,id = product_id)
    if request.method == 'POST':
        form = Product_Form(request.POST,request.FILES,instance=product_instance)
        if form.is_valid():
            form.save()
            return redirect('product_items')
    else:
        form = Product_Form(instance=product_instance)
    context={
        'form': form,
        'product': product_instance
    }
    return render(request,'products/edit_product.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_product(request,product_id):
    product_instance = get_object_or_404(Product,id = product_id)
    if request.method == 'POST':
        product_instance.delete()
        return redirect('product_items')
    context={
     'product': product_instance
    }
    return render(request,'products/delete_product.html',context)





#--------------------------------- Category --------------------------------------------------------------------#


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
  
    if request.method == 'POST':
        form = Category_Form(request.POST,request.FILES)
        if form.is_valid():
            category_instance = form.save(commit=False)
            category_instance.vendor = Vendor.objects.get(user=request.user)
            category_instance.save()
            messages.success(request, f'{Category.category_name} created successfully')
            return redirect('category_items')
    else:
        form = Category_Form()        
    context = {
        'title': 'Add new category',
        'Category_Form' : form

    }
    return render(request,'category/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def category_items(request):
    vendor = Vendor.objects.filter(user=request.user)
    category = Category.objects.filter(vendor__in=vendor)
    context = {
        'category': category
    }
    
    return render(request, 'category/category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,category_id):
    category_instance = get_object_or_404(Category,id = category_id)
    if request.method == 'POST':
        form = Category_Form(request.POST,request.FILES,instance=category_instance)
        if form.is_valid():
            form.save()
            return redirect('category_items')
    else:
        form = Category_Form(instance=category_instance)
    context={
        'form': form,
        'category': category_instance
    }
    return render(request,'category/edit_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,category_id):
    category = get_object_or_404(Category,id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_items')
    context={
     'category': category
    }
    return render(request,'category/delete_category.html',context)

#----------------------------------- Brand-----------------------------------------------#


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_brand(request):
    if request.method == 'POST':
        form = Brand_Form(request.POST, request.FILES)
        if form.is_valid():
            brand_instance = form.save(commit=False)
            brand_instance.vendor = Vendor.objects.get(user=request.user)
            brand_instance.save()
            messages.success(request, f'{Brand.brand_name} created successfully')  # Ensure you access the correct attribute
            return redirect('brand_items')
    else:
        form = Brand_Form()
        
    context = {
        'title': 'Add new brand',
        'Brand_Form': form
    }
    return render(request, 'brand/add_brand.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def brand_items(request):
    vendor = Vendor.objects.filter(user=request.user)
    brands = Brand.objects.filter(vendor__in=vendor)  # Adjusted variable name from category to brands
    context = {
        'brands': brands  # Adjusted variable name
    }
    
    return render(request, 'brand/brand.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_brand(request, brand_id):
    brand_instance = get_object_or_404(Brand, id=brand_id)  # Changed to Brand
    if request.method == 'POST':
        form = Brand_Form(request.POST, request.FILES, instance=brand_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand updated successfully')
            return redirect('brand_items')
    else:
        form = Brand_Form(instance=brand_instance)
        
    context = {
        'form': form,
        'brand': brand_instance  # Changed to brand
    }
    return render(request, 'brand/edit_brand.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_brand(request, brand_id):
    brand_instance = get_object_or_404(Brand, id=brand_id)  # Changed to Brand
    if request.method == 'POST':
        brand_instance.delete()
        messages.success(request, 'Brand deleted successfully')
        return redirect('brand_items')
        
    context = {
        'brand': brand_instance  # Changed to brand
    }
    return render(request, 'brand/delete_brand.html', context)



    
     

