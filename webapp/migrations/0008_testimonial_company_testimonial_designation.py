# Generated by Django 5.1.3 on 2024-11-12 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_partner_team_testimonial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]