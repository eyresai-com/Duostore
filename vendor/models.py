from django.db import models

from vendor.utils import send_notification
from accounts.models import *
from customer.models import *


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=1000)
    vendor_slug = models.SlugField(max_length=1000, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    vendor_description = models.TextField(null=True , blank=True)
    offical_number = models.PositiveIntegerField(null=True, blank=True)
    website = models.CharField(max_length=50 , null=True, blank=True)
    estd_year = models.PositiveIntegerField(null=True , blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    #Send notification email
                    mail_subject = "Congratulations! Your firm Portfolio has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "We're sorry! You are not eligible for publishing your Portfolio on our marketplace."
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)



#----------------------------------invoices------------------------------#
