from django import forms
from .models import *
from products.models import *

class ItemForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'brand': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Item/Product/Service Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'rows': 4, 'placeholder': 'Item/Product/Service Description'}),
            'category': forms.Select(attrs={'class': 'form-select select2', 'required': 'required'}),
            'unit_type': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Unit type (eg. Item, Hours, Pcs, etc.)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Item/Product/Service Price'}),
        }

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)  # Get the vendor from kwargs
        super(ItemForm, self).__init__(*args, **kwargs)

        if vendor is not None:
            # Filter the queryset by the vendor
            self.fields['vendor'].queryset = Vendor.objects.filter(id=vendor.id)  # Adjust this line if you have a specific way to associate products with vendors


class ItemSelectionForm(forms.Form):
    selected_item = forms.ModelChoiceField(
        queryset=Product.objects.none(),  # Start with an empty queryset
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'yourSelectInput'}),
        label="Select Product"
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Quantity"
    )

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)  # Get the vendor from kwargs
        super(ItemSelectionForm, self).__init__(*args, **kwargs)

        if vendor is not None:
            # Filter the queryset by the vendor
            self.fields['selected_item'].queryset = Product.objects.filter(vendor=vendor)

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity

    def clean_selected_item(self):
        item = self.cleaned_data.get('selected_item')
        if not item:
            raise forms.ValidationError("Please select a valid product.")
        return item


    



class otherFeeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['other_fees_name' ,'other_fees_amount']
        widgets = {
            'other_fees_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'other_fees_amount' : forms.NumberInput(attrs={'class' : 'form-control'}),
        }

# Invoice Form
class invoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['status', 'billDate' ,'dueDate', 'notes']

        widgets = {
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'rows':4}),
            'status' : forms.Select(attrs={'class':'form-select select2'}),
            'billDate' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'dueDate' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
              
                # Add widget for other_fees_name if needed

            
        }








