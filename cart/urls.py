from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.AddCartProductAPI.as_view(), name='add-product-to-cart'),
    path('remove/<int:product_id>/', views.RemoveCartProduct.as_view(), name='remove-product-from-cart'),
    path('get-cart/', views.GetCartAPI.as_view(), name='get-cart'),
    path('get-price/',views.GetCartPriceAPI.as_view(), name='get-price'),
    path('arrived/<int:cart_id>/', views.ArrivalCartAPI.as_view(), name='is-arrived'),
    path('ordered-carts/', views.GetAllOrderedCart.as_view(), name='ordered-carts'),
]