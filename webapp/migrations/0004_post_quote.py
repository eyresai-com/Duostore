# Generated by Django 5.1.3 on 2024-11-08 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_post_title1'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='quote',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
