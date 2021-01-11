from django.contrib import admin

from products.models import (
    Product, 
    RateProduct,
    ProductImage,
    ProductRateImage,
    RateProductPrice
)

admin.site.register(Product)
admin.site.register(ProductImage)

admin.site.register(RateProduct)
admin.site.register(ProductRateImage)
admin.site.register(RateProductPrice)