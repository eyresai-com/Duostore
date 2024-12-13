from django.shortcuts import render
from accounts.models import *
from vendor.models import *
from accounts.views import *


# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    pass

