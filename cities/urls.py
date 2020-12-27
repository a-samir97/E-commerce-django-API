from django.urls import path

from .views import ListCitiesAPI

app_name = 'cities'

urlpatterns = [
    path('', ListCitiesAPI.as_view(), name='get-all-cities'),
]