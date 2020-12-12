from rest_framework.routers import DefaultRouter
from .views import ProductAPIViewSet


app_name = 'products'

router = DefaultRouter()
router.register('products', ProductAPIViewSet, basename='products')
urlpatterns = router.urls
