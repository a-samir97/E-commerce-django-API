from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from rest_framework.response import Response

from .serializers import CommentSerializer
from .models import Comment

from products.models import Product

class CommentAPIViewSet(ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):

        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = (permissions.AllowAny,)
        else:
            permission_classes = (permissions.IsAuthenticated,)
        
        return [permission() for permission in permission_classes]

    def list(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        
        if product:
            queryset = product.comments.all()
            comments_serializer = CommentSerializer(queryset, many=True)
            return Response(comments_serializer.data)
        else:
            return Response(
                {'error': 'product_id is not found'},
                status=status.HTTP_404_NOT_FOUND
                )

    def create(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()

        if product:
            comment_serializer = CommentSerializer(data=request.data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(comment_serializer.data)
        else:
            return Response(
                {'error': 'product_id is not found'},
                status=status.HTTP_404_NOT_FOUND
                )

    