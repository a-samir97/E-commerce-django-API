from django.db import models
from django.conf import settings

from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    is_ordered = models.BooleanField(default=False)
    is_arrived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} cart'.format(self.user.first_name)
    
    def calculate_price(self):
        total_price = 0
        products = self.products.all()
        for product in products:
            total_price += product.product.price * product.quantity
        return total_price
    
    def calculate_taxes(self):
        total_price = self.calculate_price()
        taxes = (4/100) * total_price
        return taxes

    def calculate_total_price(self):
        return self.calculate_taxes() + self.calculate_price()
        
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')

    def __str_(self):
        return '{} in cart {}'.format(self.product.name, self.cart.id)