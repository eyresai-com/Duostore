from django import forms
from .models import *

class Product_Form(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['vendor','slug']

    def __init__(self, *args, **kwargs):
        super(Product_Form, self).__init__(*args, **kwargs)

        # Set all fields as not required
        for field in self.fields.values():
            field.required = False

class Category_Form(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['vendor']
    
    def __init__(self, *args, **kwargs):
        super(Category_Form, self).__init__(*args, **kwargs)

        # Set all fields as not required
        for field in self.fields.values():
            field.required = False


class Brand_Form(forms.ModelForm):
    class Meta:
        model = Brand
        exclude = ['vendor']

        
    def __init__(self, *args, **kwargs):
        super(Brand_Form, self).__init__(*args, **kwargs)

        # Set all fields as not required
        for field in self.fields.values():
            field.required = False