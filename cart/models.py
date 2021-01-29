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

    # def calculate_total_price(self):
    #     return self.calculate_taxes() + self.calculate_price()

    def calculate_shipping_price(self):
        total_shipping = 0
        products = self.products.all()
        for product in products:
            if product.product.weight <= 15.00:
                total_shipping += ((15/100) * 28)+ 28 + 10
                return total_shipping
            elif product.product.weight== 16:
                total_shipping += ((15/100) * 30) + 30 + 10
                return total_shipping
            elif product.product.weight== 17:
                total_shipping += ((15/100) * 32) + 32 + 10
                return total_shipping
            elif product.product.weight== 18:
                total_shipping += ((15/100) * 34) + 34 + 10
                return total_shipping
            elif product.product.weight== 19:
                total_shipping += ((15/100) * 36) + 36 + 10
                return total_shipping
            elif product.product.weight== 20:
                total_shipping += ((15/100) * 36) + 38 + 10
                return total_shipping
            elif product.product.weight > 20:
                total_shipping += ((15/100) * 40) + 40 + 10
                return total_shipping
        return total_shipping

    def calculate_shipping_cash_price(self):
        total_shipping = 0
        products = self.products.all()
        for product in products:
            if product.product.weight <= 15.00:
                total_shipping += ((15/100) * 28) + 28 + 10 + 15
                return total_shipping
            elif product.product.weight == 16:
                total_shipping += ((15/100) * 30) + 30 + 10 + 15
                return total_shipping
            elif product.product.weight == 17:
                total_shipping += ((15/100) * 32) + 32 + 10 + 15
                return total_shipping
            elif product.product.weight == 18:
                total_shipping += ((15/100) * 34)+ 34 + 10 + 15
                return total_shipping
            elif product.product.weight == 19:
                total_shipping += ((15/100) * 36) + 36 + 10 + 15
                return total_shipping
            elif product.product.weight == 20:
                total_shipping += ((15/100) * 38) + 38 + 10 + 15
                return total_shipping
            elif product.product.weight > 20:
                total_shipping += ((15/100) * 40) + 40 + 10 + 15
                return total_shipping
        return total_shipping

    def calculate_total_price(self):
        return self.calculate_taxes() + self.calculate_price()

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_arrived = models.BooleanField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')

    def __str_(self):
        return '{} in cart {}'.format(self.product.name, self.cart.id)