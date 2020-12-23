from rest_framework import serializers

from users.models import User
from products.models import Product, RateProduct
from comments.models import Comment
from reviews.models import Review

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

class DashboardProductSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = '__all__'
    
class DashboardRateProductSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = RateProduct
        fields = "__all__"

class DashboardCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'

class DashboardReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField()
    review_for = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = '__all__'