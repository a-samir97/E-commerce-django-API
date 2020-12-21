from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('create-review/<int:user_id>/', views.CreateReviewAPI.as_view(), name='create-review'),
    path('update-review/<int:pk>/', views.UpdateReviewAPI.as_view(), name='update-review'),
    path('delete-review/<int:pk>/', views.DeleteReviewAPI.as_view(), name='delete-review')
]