from django.db import models

from users.models import User

class Product(models.Model):
    img = models.ImageField(upload_to='media/')
    city = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.TextField()
    is_new = models.BooleanField(default=False)
    is_fixed = models.BooleanField(default=True)
    price = models.IntegerField(default=0)
    duration = models.DateTimeField(null=True, blank=True)
    sold_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name