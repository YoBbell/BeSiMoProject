from django.contrib import admin
from .models import Products, Category, Customer, Order
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'store', 'location', 'image_tag']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.image.url))

    image_tag.short_description = 'Image'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# Register your models here.
admin.site.register(Products, ProductAdmin)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
