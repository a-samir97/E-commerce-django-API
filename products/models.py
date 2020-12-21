from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from categories.models import SubCategory

class Product(models.Model):
    img = models.ImageField(upload_to='media/')
    city = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.TextField()

    is_new = models.BooleanField(default=False)
    is_fixed = models.BooleanField(default=True)

    price = models.IntegerField(default=0)
    bidding_limit = models.IntegerField(default=0)

    duration = models.DateTimeField(null=True, blank=True)

    sold_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class RateProduct(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rated_products')
    is_rated = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name