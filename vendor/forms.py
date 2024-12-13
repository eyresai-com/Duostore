from django import forms
from .models import *

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_description','vendor_license','offical_number','website','estd_year']
       