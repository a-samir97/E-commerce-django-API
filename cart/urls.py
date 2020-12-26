from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.AddCartProductAPI.as_view(), name='add-product-to-cart'),
    path('remove/<int:product_id>/', views.RemoveCartProduct.as_view(), name='remove-product-from-cart'),
    path('get-cart/', views.GetCartAPI.as_view(), name='get-cart')
]