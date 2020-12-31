from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('get-reviews/', views.GetCurrentUserReviews.as_view(), name='user-reviews'),
    path('get-reviews/<int:user_id>/',views.GetUserReviews.as_view(), name='get-user-reviews'),
    path('get-user-data/<int:pk>/',views.GetUserData.as_view(), name='get-user-data')    
]