from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    ProductAPIViewSet,
    ToggleFavoriteProductAPI,
    BiddingProductAPI,
    AutomaticBiddingProductAPI,
    FixedPriceProducts,
    VariablePriceProducts,
    LatestProducts,
    RequestRateProduct,
    HighPriceProducsts,
    LowPriceProducts,
    SearchByCategory,
    SearchBySubCategory,
    SearchByName,
    GetUserFavoriteProductsAPI,
    EndProductDuration,
    GetAllRatedProduct
)


app_name = 'products'

router = DefaultRouter()
router.register('', ProductAPIViewSet, basename='products')

urlpatterns = [
    path('favorite/<int:product_id>/', ToggleFavoriteProductAPI.as_view(), name='fav-products'),
    path('bidding/<int:product_id>/', BiddingProductAPI.as_view(), name='bidding-product'),
    path('automatic-bidding/<int:product_id>/',AutomaticBiddingProductAPI.as_view(), name='automatic-bidding'),
    path('all-fixed-products/', FixedPriceProducts.as_view(), name='products-fixed-price'),
    path('all-bidding-products/', VariablePriceProducts.as_view(), name='bidding-products'),
    path('latest-products/', LatestProducts.as_view(), name='latest-products'),
    path('high-price-products/',HighPriceProducsts.as_view(), name='high-price-products'),
    path('low-price-products/', LowPriceProducts.as_view(), name='low-price-products'),
    path('search-category/', SearchByCategory.as_view(), name='search-by-category'),
    path('search-subcategory/', SearchBySubCategory.as_view(), name='search-by-sub-category'),
    path('search-name/', SearchByName.as_view(), name='search-by-name'),
    path('get-favorite-products/', GetUserFavoriteProductsAPI.as_view(), name='get-favorite-products'),
    path('end/<int:product_id>/', EndProductDuration.as_view(), name='end-time'),

    path('rate-product/', RequestRateProduct.as_view(), name='rate-products'),
    path('all-rated-products/', GetAllRatedProduct.as_view(), name='list-rated-products'),

]

urlpatterns += router.urls
