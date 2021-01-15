from rest_framework import serializers

from .models import CartItem, Cart
from products.models import Product
from cities.serializers import CitySerializer
from categories.serializers import CategorySerializer, SubCategorySerializer
from products.serializers import ProductImageSerializer
from users.serializers import UserDataSerializer

class ProductItemSerializers(serializers.ModelSerializer):
    city = CitySerializer()
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    images = serializers.SerializerMethodField()
    owner = UserDataSerializer()
    
    def get_images(self, obj):
        serializer = ProductImageSerializer(obj.images.all(), many=True)
        return serializer.data
    
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializers(serializers.ModelSerializer):
    product = ProductItemSerializers()
    class Meta:
        model = CartItem
        fields = '__all__' 

class CartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'products')
    
    def get_products(self, obj):
        serializer = CartItemSerializers(obj.products.all(), many=True)
        return serializer.data