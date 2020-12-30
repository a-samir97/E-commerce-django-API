from rest_framework import serializers

from .models import Comment
from users.serializers import UserDataSerializer

class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)
        
class CommentSerializer(serializers.ModelSerializer):
    author = UserDataSerializer()
    class Meta:
        model = Comment
        fields = '__all__'