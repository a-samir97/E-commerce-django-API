from rest_framework import serializers

from .models import Review

from users.serializers import UserDataSerializer

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('created_at', 'approved', 'reviewer', 'review_for')

class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('created_at', 'approved', 'reviewer', 'review_for')

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserDataSerializer()
    class Meta:
        model = Review
        exclude = ('review_for',)