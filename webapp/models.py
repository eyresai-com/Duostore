from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.utils import timezone


# Create your models here.


User = get_user_model()

class Post(models.Model):
	title = models.CharField(max_length=100)
	short_content = models.TextField()
	title1 = models.CharField(max_length=100 , null=True , blank=True)
	content = models.TextField()
	quote = models.CharField(max_length=1000 , null=True , blank=True)
	title2 = models.CharField(max_length=100 , null=True , blank=True)
	content1 = models.TextField(null=True , blank=True)
	image = models.ImageField(upload_to='blog/', blank=True, null=True)
	banner_image = models.ImageField(upload_to='blog/', blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey('Category', null=True,  on_delete=models.SET_NULL)
	created = models.DateTimeField(default=timezone.now)
	tags = TaggableManager(blank=True)


	def __str__(self):
		return self.title




class Category(models.Model):
	category_name = models.CharField(max_length=50)



	class Meta:
		verbose_name = 'category'
		verbose_name_plural = 'categories'


	def __str__(self):
		return self.category_name





class ContactDetails(models.Model):
    # location = 
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)


    def __str__(self):
        return str(self.id)
	

class Testimonial(models.Model):
	name = models.CharField(max_length=100, null=True , blank=True)
	image = models.ImageField(upload_to='blog/', blank=True, null=True)
	content = models.TextField(null=True, blank=True)
	designation = models.CharField(max_length=100, null=True , blank=True)
	company = models.CharField(max_length=100, null=True , blank=True)

	def __str__(self):
		return str(self.name)
	


class Pro_Overview(models.Model):
	name = models.CharField(max_length=100, null=True , blank=True)
	image = models.ImageField(upload_to='blog/', blank=True, null=True)

	def __str__(self):
		return str(self.name)
	
	

class Team(models.Model):
	name = models.CharField(max_length=100, null=True , blank=True)
	image = models.ImageField(upload_to='blog/', blank=True, null=True)
	designation = models.CharField(max_length=100, null=True , blank=True)
	facbook_link = models.URLField(max_length=100, null=True , blank=True)
	twitter_link = models.URLField(max_length=100, null=True , blank=True)
	instagram_link = models.URLField(max_length=100, null=True , blank=True)
	linkedin_link = models.URLField(max_length=100, null=True , blank=True)





	def __str__(self):
		return str(self.name)
	

class Partner(models.Model):
	name = models.CharField(max_length=100, null=True , blank=True)
	image = models.ImageField(upload_to='blog/', blank=True, null=True)


	def __str__(self):
		return str(self.name)