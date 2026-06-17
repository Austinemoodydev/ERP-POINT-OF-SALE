from django.contrib import admin

from .models import (
    Category,
    Brand,
    Unit,
    Product,
    ProductVariation,
    ProductImage,
    ProductLocation,
    StockLevel,
)

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(ProductVariation)
admin.site.register(ProductImage)
admin.site.register(ProductLocation)
admin.site.register(StockLevel)
