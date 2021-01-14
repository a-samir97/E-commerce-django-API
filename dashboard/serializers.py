from rest_framework import serializers

from users.models import User
from products.models import Product, RateProduct, RateProductPrice
from comments.models import Comment
from reviews.models import Review

from cities.serializers import CitySerializer
from categories.models import SubCategory
from categories.serializers import CategorySerializer

class DashboardUpdateRateProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateProductPrice
        exclude = ('name',)
        
class DashboardRateProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateProductPrice
        fields = '__all__'

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
            "company_address","is_blocked","is_gold"
        )
    
class DashboardRateProductSerializer(serializers.ModelSerializer):
    owner = DashboardUserSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = RateProduct
        fields = "__all__"

    def get_total_price(self, obj):
        return obj.calculate_user_pay()
        
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