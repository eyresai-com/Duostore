from django.shortcuts import render , redirect
from .models import *
from django.core.mail import send_mail , BadHeaderError
from django.http import HttpResponse  , HttpResponseRedirect
from .forms import ContactForm
from django.core.mail import send_mail as sm

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



def privacy_policy(request):
    return render(request , 'webapp/p_policy.html')




def terms(request):
    return render(request , 'webapp/terms.html')




def cancellation(request):
    return render(request , 'webapp/cancel.html')


def shipping(request):
    return render(request , 'webapp/shipping.html')

     