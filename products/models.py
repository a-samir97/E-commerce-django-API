from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from categories.models import Category, SubCategory
from cities.models import City

################################################
############### Product Model ##################
################################################

class Product(models.Model):
    city = models.ForeignKey(City, default=1, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=30)
    description = models.TextField()

    is_new = models.BooleanField(default=True)
    is_fixed = models.BooleanField(default=True)

    price = models.IntegerField(default=0)
    bidding_limit = models.IntegerField(default=0)

    duration = models.DateTimeField(null=True, blank=True)
    in_stock = models.IntegerField(default=1)
    size = models.FloatField(default=0.0)
    
    last_user_bid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    sold_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # fields 
    size = models.CharField(max_length=20, null=True, blank=True)
    height = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    brand = models.CharField(max_length=20, null=True, blank=True)
    warranty = models.CharField(max_length=20, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to='media/')

################################################
########### RateProduct Model ##################
################################################

class RateProduct(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rated_products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='rate_products', null=True)
    is_rated = models.BooleanField(default=False)
    uploaded_photo = models.BooleanField(default=True)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def calculate_user_pay(self):
        if self.uploaded_photo:
            price = self.category.uploaded_price
            total = price + self.category.price
            total = total + (total * 4 / 100)
            return total
        else:
            price = self.category.msawm_team_price
            total = price + self.category.price
            total = total + (total * 4 / 100)
            return total

class ProductRateImage(models.Model):
    rate_product = models.ForeignKey(RateProduct, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to='media/')