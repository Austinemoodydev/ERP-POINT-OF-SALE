from django.contrib import admin
from django.utils.html import format_html

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
admin.site.register(ProductVariation)
admin.site.register(ProductImage)
admin.site.register(ProductLocation)
admin.site.register(StockLevel)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["barcode_preview"]

    def barcode_preview(self, obj):
        if obj.barcode_image:
            return format_html(
                '<img src="{}" width="150"/>',
                obj.barcode_image.url
            )
        return "-"
    barcode_preview.short_description = "Barcode"
