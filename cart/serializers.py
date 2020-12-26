from rest_framework import serializers

from .models import CartItem
from products.models import Product

class ProductItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description')

class CartItemSerializers(serializers.ModelSerializer):
    product = ProductItemSerializers()
    class Meta:
        model = CartItem
        fields = '__all__' 