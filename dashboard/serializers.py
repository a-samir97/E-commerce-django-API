from rest_framework import serializers

from users.models import User
from products.models import Product, RateProduct , ProductRateImage
from comments.models import Comment
from reviews.models import Review

from cities.serializers import CitySerializer
from categories.models import SubCategory
from categories.serializers import CategorySerializer


class DashboardUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('owner',)
        
class DashboardListSubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = SubCategory
        fields = '__all__'

class DashboardSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class DashboardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'email', 'phone_number',
            'user_type',"show_name","gender",
            "location","is_company","company_name",
            "company_address","is_blocked","is_gold" , 
            "global_visa","local_visa","bank_name"
        )

class RateProductImageSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = ProductRateImage
        exclude = ('rate_product',)

    def get_img(self, obj):
        return obj.img.url

class DashboardRateProductSerializer(serializers.ModelSerializer):
    owner = DashboardUserSerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = RateProduct
        fields = "__all__"

    # def get_total_price(self, obj):
    #     return obj.calculate_user_pay()

    def get_images(self, obj):
        serializer = RateProductImageSerializer(obj.images.all(), many=True)
        return serializer.data

class DashboardUpdateRateProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RateProduct
        exclude = ('owner', )

class DashboardCommentSerializer(serializers.ModelSerializer):
    author = DashboardUserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'

class DashboardReviewSerializer(serializers.ModelSerializer):
    reviewer = DashboardUserSerializer()
    review_for = DashboardUserSerializer()
    
    class Meta:
        model = Review
        fields = '__all__'