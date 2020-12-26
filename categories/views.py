from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer

class ListAllCategories(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)

class ListAllSubcategories(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, category_id):
        try:
            category_object = Category.objects.get(id=category_id)
            subcategories = category_object.all_subcategories.all()
            serializer = SubCategorySerializer(subcategories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response (
                {'error': 'category id is not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
