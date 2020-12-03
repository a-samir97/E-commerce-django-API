from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
]