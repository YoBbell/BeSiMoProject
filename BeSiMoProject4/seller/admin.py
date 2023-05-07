from django.contrib import admin
from .models import *
from django.utils.html import format_html


# class AdminProduct(admin.ModelAdmin):
#     list_display = ['name', 'price', 'category', 'store', 'location', 'image_tag']

#     def image_tag(self, obj):
#         return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.image.url))

#     image_tag.short_description = 'Image'


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name']

class SellerAdmin(admin.ModelAdmin):
    list_display = ["store_name"]

# Register your models here.
admin.site.register(Seller)
admin.site.register(Item)
admin.site.register(Category)


