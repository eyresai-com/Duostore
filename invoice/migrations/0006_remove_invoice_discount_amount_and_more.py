# Generated by Django 5.1.2 on 2024-10-28 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_remove_invoice_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='discount_amount',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='tax_amount',
        ),
    ]
