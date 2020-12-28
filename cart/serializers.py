from rest_framework import serializers

from .models import CartItem
from products.models import Product
from cities.serializers import CitySerializer
from categories.serializers import CategorySerializer, SubCategorySerializer

class ProductItemSerializers(serializers.ModelSerializer):
    city = CitySerializer()
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    class Meta:
        model = Product
        fields = '__all__'
        
class CartItemSerializers(serializers.ModelSerializer):
    product = ProductItemSerializers()
    class Meta:
        model = CartItem
        fields = '__all__' 