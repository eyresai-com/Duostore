# Generated by Django 5.1.2 on 2024-10-22 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
        ('vendor', '0002_rename_experience_vendor_estd_year_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='client',
        ),
        migrations.AddField(
            model_name='invoice',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor'),
        ),
    ]