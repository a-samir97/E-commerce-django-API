from django.contrib import admin

from products.models import Product, RateProduct

admin.site.register(Product)
admin.site.register(RateProduct)