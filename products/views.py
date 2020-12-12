from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .serializers import ProductSerializer
from .models import Product

class ProductAPIViewSet(ModelViewSet):

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = (permissions.AllowAny,)
        else:
            permission_classes = (permissions.IsAuthenticated,)
        return [permission() for permission in permission_classes]
        
    serializer_class = ProductSerializer
    queryset = Product.objects.all()