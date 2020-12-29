from rest_framework import serializers
from .models import (
    Product,
    ProductImage,
    ProductRateImage,
    RateProduct
)

from cities.serializers import CitySerializer
from categories.serializers import CategorySerializer, SubCategorySerializer

######################################
########## ProductSerializer #########
######################################

class ProductImageSerializer(serializers.ModelSerializer):    
    img = serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        exclude = ('product',)

    def get_img(self, obj):
        return obj.img.url

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    city = CitySerializer()
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    last_user_bid = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
    
    def get_images(self, obj):
        serializer = ProductImageSerializer(obj.images.all(), many=True)
        return serializer.data

    def get_last_user_bid(self, obj):
        if obj.last_user_bid:
            return obj.last_user_bid.first_name + ' ' + obj.last_user_bid.last_name
        else:
            None

class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'sold_to', 'owner')

    def get_images(self, obj):
        serializer = ProductImageSerializer(obj.images.all(), many=True)
        return serializer.data

######################################
########## RateProductSerializer #####
######################################

class RateProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRateImage
        exclude = ('rate_product',)

class CreateRateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateProduct
        exclude = ('price', 'is_rated', 'owner')