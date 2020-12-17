from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    ProductAPIViewSet,
    ToggleFavoriteProductAPI,
    BiddingProductAPI,
    AutomaticBiddingProductAPI,
    FixedPriceProducts,
    VariablePriceProducts,
    LatestProducts
)


app_name = 'products'

router = DefaultRouter()
router.register('', ProductAPIViewSet, basename='products')

urlpatterns = [
    path('favorite/<int:product_id>', ToggleFavoriteProductAPI.as_view(), name='fav-products'),
    path('bidding/<int:product_id>', BiddingProductAPI.as_view(), name='bidding-product'),
    path('automatic-bidding/<int:product_id>',AutomaticBiddingProductAPI.as_view(), name='automatic-bidding'),
    path('all-fixed-products/', FixedPriceProducts.as_view(), name='products-fixed-price'),
    path('all-bidding-products/', VariablePriceProducts.as_view(), name='bidding-products'),
    path('latest-products/', LatestProducts.as_view(), name='latest-products')
]

urlpatterns += router.urls
