from rest_framework.generics import ListAPIView
from rest_framework import permissions

from .models import City
from .serializers import CitySerializer

class ListCitiesAPI(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (permissions.AllowAny,)