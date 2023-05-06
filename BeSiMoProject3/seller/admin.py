from django.contrib import admin
from seller.models import *
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'seller', 'location', 'image_tag']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.image.url))

    image_tag.short_description = 'Image'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class SellerAdmin(admin.ModelAdmin):
    list_display = ["store_name", "location"]

    def __str__(self):
        return self.store_name

# Register your models here.
admin.site.register(Seller, SellerAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(Category, CategoryAdmin)



