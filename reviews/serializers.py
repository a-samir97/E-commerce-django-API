from rest_framework import serializers

from .models import Review

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('created_at', 'approved', 'reviewer', 'review_for')

class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('created_at', 'approved', 'reviewer', 'review_for')

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField()
    class Meta:
        model = Review
        exclude = ('review_for',)