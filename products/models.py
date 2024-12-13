from django.db import models
from vendor.models import *
from django.utils.text import slugify
import random,string

product_type=(
    ('Online',"Online"),
    ('Offline',"Offline"),
    ('Both',"Both"),
)



class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_category',null=True, blank=True)
    category_name = models.CharField(max_length=1000, null=True, blank=True)
    tax = models.DecimalField(decimal_places=1,max_digits=10, null=True)
    image = models.ImageField(upload_to = 'vendor/category',null = True, blank = True) 
    
    def __str__(self):
        return self.category_name

class Brand(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_brand',null=True, blank=True)
    brand_name = models.CharField(max_length=1000, null=True, blank=True)
    brand_image= models.ImageField(upload_to = 'products/brands', null=True , blank=True)

    def __str__(self):
        return self.brand_name

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,related_name='vendor_products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category_products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name='brand_products')
    slug = models.SlugField(max_length=1000, unique=True,null = True, blank = True)
    product_name = models.CharField(max_length=1000, null=True, blank=True)
    product_price = models.DecimalField(decimal_places=2,max_digits=10, null=True)
    discounted_price = models.DecimalField(decimal_places=3,max_digits=10, null=True) 
    description = models.TextField()
    specification = models.TextField(null=True, blank=True)
    Breif_description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to = 'vendor/product',null = True, blank = True) 
    unit_type = models.CharField(max_length=1000, null=True, blank=True)
    pro_type= models.CharField(choices=product_type,max_length=1000,null = True, blank = True)

    def generate_unique_slug(self, base_slug):
        # Generate a random 3-character string
        random_chars = ''.join(random.choices(string.ascii_lowercase, k=3))
        return f"{base_slug}-{random_chars}"

    def save(self, *args, **kwargs):
        # Generate the initial slug from the item's name
        base_slug = slugify(self.product_name)
        slug = base_slug
        count = 1

        while Product.objects.filter(slug=slug).exists():
            # Slug conflict exists, add an extra number to the slug
            slug = f"{base_slug}-{count}"
            count += 1

        self.slug = slug
        super().save(*args, **kwargs)
       
    
    def __str__(self):
        return self.product_name or 'Unnamed Product'
    




class Product_images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to = 'vendor/product',null = True, blank = True) 

    def __str__(self):
        return self.product.product_name or 'Unnamed Product'



    
    

               