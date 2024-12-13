from invoice.models import *
from vendor.models import *
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save



# Create your models here.
class Payment(models.Model):
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.SET_NULL, related_name='payments')
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    payment_method = models.CharField(max_length=300, blank=True, null=True)
    payment_amount = models.FloatField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    payment_note = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)
            
    def __str__(self):
        return f"Invoice: {self.invoice}, Title: {self.title}"
    



# CRM Expense
class Expense(models.Model):
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.CASCADE)

    date_of_expense = models.DateField(blank=True, null=True)
    EXPENSE_TYPE = (
    ('rent/mortgage', 'Rent/Mortgage'),
    ('utilities', 'Utilities'),
    ('transportation', 'Transportation'),
    ('food_and_dining', 'Food and Dining'),
    ('insurance', 'Insurance'),
    ('taxes', 'Taxes'),
    ('debt_payments', 'Debt Payments'),
    ('healthcare_and_medical_expenses', 'Healthcare and Medical Expenses'),
    ('miscellaneous_expenses', 'Miscellaneous Expenses'),
    ('personal_care', 'Personal Care'),
    ('fees', 'Fees'),
    ('others', 'Others'),
)
    category = models.CharField(max_length=300, blank=True, null=True, choices=EXPENSE_TYPE)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, blank=True, null=True)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = slugify(self.title)
            unique_slug = original_slug
            suffix = 1

            while Expense.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{original_slug}-{suffix}"
                suffix += 1

            self.slug = unique_slug
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

