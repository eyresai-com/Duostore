from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from products.models import *
from vendor.models import *
from django.core.mail import send_mail , BadHeaderError
from django.http import HttpResponse  , HttpResponseRedirect
from .forms import ContactForm
from django.core.mail import send_mail as sm
from django.db.models import Count , Q


# Create your views here.



def home(request):
    team_list = Team.objects.all()
    partner_list = Partner.objects.all()
    testimonial_list = Testimonial.objects.all()
    post_list = Post.objects.all()

    context = { 
        'team_list' : team_list ,
        'partner_list' : partner_list , 
        'testimonial_list' : testimonial_list ,
        'post_list' : post_list ,
    
    }
    
    return render(request, 'webapp/index.html', context)






def about(request):
    team_list = Team.objects.all()
    partner_list = Partner.objects.all()
    testimonial_list = Testimonial.objects.all()

    context = { 
        'team_list' : team_list ,
        'partner_list' : partner_list , 
        'testimonial_list' : testimonial_list ,
    
    }


    return render(request, 'webapp/about.html', context)


def prods(request):
    vendor_list = Vendor.objects.filter(is_approved=True)
    # Fetch all brands and categories, then remove duplicates manually
    brands = Brand.objects.all()
    categories = Category.objects.all()

    # Filter unique brands and categories
    unique_brands = {}
    for brand in brands:
        if brand.brand_name not in unique_brands:
            unique_brands[brand.brand_name] = brand

    unique_categories = {}
    for category in categories:
        if category.category_name not in unique_categories:
            unique_categories[category.category_name] = category


    post_list = Post.objects.all()


    context = { 
        'vendor_list': vendor_list , 
        'post_list' : post_list ,
        'categories' : categories ,
        'brands' : brands ,
         
    }
    return render(request, 'webapp/prods.html' , context)



def prods_detail(request, vendor_slug):
    vendor_detail = get_object_or_404(Vendor, vendor_slug=vendor_slug, is_approved=True)

    categories = Category.objects.filter(vendor=vendor_detail)

    brands = Brand.objects.filter(vendor=vendor_detail)

    categories_with_count = categories.annotate(product_count=Count('category_products', filter=Q(category_products__vendor=vendor_detail)))

    brands_with_count = brands.annotate(product_count=Count('brand_products', filter=Q(brand_products__vendor=vendor_detail)))


    selected_category_id = request.GET.get('category')
    selected_brand_id = request.GET.get('brand')


    if selected_category_id:
        products = Product.objects.filter(vendor=vendor_detail, category_id=selected_category_id)
    else:
        products = Product.objects.filter(vendor=vendor_detail)

    if selected_brand_id:
            products = products.filter(brand_id=selected_brand_id)



    context = { 
        'vendor_detail': vendor_detail , 
        'products': products,
        'brands': brands_with_count,
        'categories': categories_with_count,
        'selected_category_id': int(selected_category_id) if selected_category_id else None,
        'selected_brand_id': int(selected_brand_id) if selected_brand_id else None,

    }

         
    return render(request, 'webapp/prods_detail.html' , context)



def product_detail(request, product_slug):
    # Fetch the product details by slug
    product = get_object_or_404(Product, slug=product_slug)

    product_imgs= Product_images.objects.filter(product=product)
    # Fetch related products (optional, e.g., from the same category)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]  # Limit to 4 related products



    context = {
        'product': product,
        'related_products': related_products,
        'product_imgs': product_imgs,
    }

    return render(request, 'webapp/product_detail.html', context)





def overview(request):
    pro_list = Pro_Overview.objects.all()

    context = {
        'pro_list' : pro_list ,
    }
    return render(request , 'webapp/overview.html' , context)



def post_list(request):
	post_list = Post.objects.all()



	context = {

		'post_list': post_list ,


	}


	return render(request , 'webapp/post_list.html', context)



def post_detail(request, id):
	post_detail = Post.objects.get(id=id)
	categories = Category.objects.all()
	post_list = Post.objects.all()


	context = {
		'post_detail': post_detail , 
        'categories' : categories ,
        'post_list': post_list,

	}

	return render(request , 'webapp/post_detail.html', context)




def post_by_tag(request, tag):
	post_by_tag = Post.objects.filter(tags__name__in=[tag])

	context = {
		'post_list':post_by_tag


	}

	return render(request , 'webapp/post_list.html', context)







def post_by_category(request, category):
	post_by_category = Post.objects.filter(category__category_name__in=[category])
	post_count = Post.objects.filter(category__category_name__in=[category]).count()

	context = {
		'post_list':post_by_category ,
        'post_count' : post_count ,


	}

	return render(request , 'webapp/post_list.html', context)



def contact(request):
    contactdetails = ContactDetails.objects.last()
    template = 'webapp/contact.html'

    if request.method == 'POST' : 
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            subject = contact_form.cleaned_data['subject']
            from_email = contact_form.cleaned_data['from_email']
            message = contact_form.cleaned_data['message']

            try : 
                sm(subject , message ,from_email , ['bharath@livingedge.in'] )
            
            except BadHeaderError : 
                return HttpResponse('ivalid header')

            return redirect('contact')

    else:
        contact_form = ContactForm()


    context = {
        'contactdetails' : contactdetails  , 
        'contact_form' : contact_form
    }


    return render(request, template , context)




