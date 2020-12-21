from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Review

from users.models import User

class CreateReviewAPI(CreateAPIView):
    serializer_class = serializers.CreateReviewSerializer

    def create(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'user is not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = serializers.CreateReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reviewer=request.user, review_for=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateReviewAPI(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.UpdateReviewSerializer

class DeleteReviewAPI(DestroyAPIView):
    queryset = Review.objects.all()