from rest_framework import serializers
from .models import Product, RateProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')

class CreateRateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateProduct
        exclude = ('price', 'is_rated', 'owner')