from django import forms
from .models import *
from invoice.models import *



# Payment Form
class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['vendor' , 'slug']         
        widgets = {
            'invoice': forms.Select(attrs={'class': 'form-select select2'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Payment Method'}),
            'payment_ammount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Payment Amount'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Payment Date'}),
            'payment_note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Payment Note', 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super(PaymentsForm, self).__init__(*args, **kwargs)
        # Customize the invoice field to display invoice numbers
        self.fields['invoice'].queryset = Invoice.objects.all()  # Load all invoices
        self.fields['invoice'].label_from_instance = lambda obj: f"Invoice #{obj.number}"

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['vendor' , 'slug']         
        widgets = {
            'date_of_expense': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date of Expense'}),
            'category': forms.Select(attrs={'class': 'form-select select2'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'amount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Expense Amount'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 4}),
        }
