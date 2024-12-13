from django.db import models
from django.utils import timezone
from uuid import uuid4
from django.utils.text import slugify
from accounts.views import *
from accounts.models import *
from products.models import Product
from decimal import Decimal  # Import Decimal for precise calculations
from num2words import num2words  # Import the num2words package


# Create your models here.


class Invoice(models.Model):
    STATUS = [
    ('UNPAID', 'UNPAID'),
    ('PAID', 'PAID'),
    ]

    number = models.CharField(null=True, blank=True, max_length=100)
    billDate = models.DateField(null=True, blank=True)
    dueDate = models.DateField(null=True, blank=True)
    status = models.CharField(choices=STATUS, default='UNPAID', max_length=100)
    other_fees_amount = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)
    other_fees_name = models.CharField(max_length=300, default="Other Fees", null=True, blank=True)
    notes = models.TextField(null=True, blank=True, default='This is a computer generated invoice no need signature')

    #RELATED fields
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.CASCADE)
   
    products = models.ManyToManyField(Product, related_name='invoice_related_items', blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        if self.number:
            return self.vendor.vendor_name
        else:
            return "None"



    def save(self, *args, **kwargs):
    # Auto-generate invoice number if not present
        if not self.number:
            latest_invoice = Invoice.objects.order_by('id').last()
            next_number = f"INV-{(latest_invoice.id if latest_invoice else 0) + 1}"
            self.number = next_number

    # Generate slug based on the invoice number
        if self.number:
            self.slug = slugify(self.number)

    # Generate a uniqueId if not present
        if not self.uniqueId:
            self.uniqueId = str(uuid4()).split('-')[4]

        super().save(*args, **kwargs)

       
    def get_total(self):
        sub_total = self.sub_total or 0
        other_fees_amount = self.other_fees_amount or 0

        total = (sub_total + other_fees_amount)
        return total

    def get_total_in_words(self):
        total = self.get_total()  # Get the total amount
        return num2words(total, to='currency', lang='en') 
    

    

   
    @classmethod
    def delete_blank_invoices(cls):
        two_hours_ago = timezone.now() - timezone.timedelta(hours=1)
        blank_invoices_to_delete = cls.objects.filter(
            products__isnull=True,
            date_created__lt=two_hours_ago
        )

        for invoice in blank_invoices_to_delete:
            invoice.delete()
       
    def get_status(self):
        # Check if the invoice is overdue based on the date
        if self.dueDate is not None and self.dueDate < timezone.now().date():
            if self.status != 'PAID':
                self.status = 'OVERDUE'

        # Set default values for sub_total, discount_amount, tax_amount, and other_fees_amount
        total_product_price = self.sub_total or 0
        other_fees_amount = self.other_fees_amount or 0

        # Calculate total after subtracting discount
        total_product_price += other_fees_amount

        total_payments = self.payments.aggregate(total=models.Sum('payment_ammount'))['total'] or 0

        # Calculate balance
        balance = total_product_price - total_payments

        if balance == 0 and total_product_price > 0:
            self.status = 'PAID'
        elif balance < 0:
            self.status = 'PAID'
        elif balance > 0:
            if self.dueDate is None or self.dueDate >= timezone.now().date():
                self.status = 'UNPAID'
            else:
                self.status = 'OVERDUE'

        self.save()

        return {"status": self.status, "balance": balance}

   
class InvoiceItem(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.item.name} - Quantity: {self.quantity} - Invoice: #{self.invoice}"