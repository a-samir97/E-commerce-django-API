from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('all-categories/', views.ListAllCategories.as_view(), name='all-categories'),
    path('all-subcategories/<int:category_id>/',views.ListAllSubcategories.as_view(), name='all-subcategories')
]