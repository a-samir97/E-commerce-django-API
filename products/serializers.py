from rest_framework import serializers
from .models import (
    Product,
    ProductImage,
    ProductRateImage,
    RateProduct
)

######################################
########## ProductSerializer #########
######################################

class ProductImageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = ProductImage
        exclude = ('product',)

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_images(self, obj):
        serializer = ProductImageSerializer(obj.images.all(), many=True)
        return serializer.data

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer()
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'sold_to', 'owner')


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