"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from payment.views import PaymentRequest
schema_view = get_schema_view(
   openapi.Info(
      title="E-commerce API",
      default_version='v1',
      description="E-commerce API V1",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-users/', include('users.urls', namespace='users')),
    path('api-products/', include('products.urls', namespace='products')),
    path('api-comments/', include('comments.urls', namespace='comments')),
    path('api-dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('api-reviews/', include('reviews.urls', namespace='reviews')),
    path('api-categories/', include('categories.urls', namespace='categories')),
    path('api-cart/', include('cart.urls', namespace='cart')),
    path('api-cities/',include('cities.urls', namespace='cities')),
    path('api-payment/', PaymentRequest.as_view()),
    path('payment/',include('payment.urls')),
    
    # swagger documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

