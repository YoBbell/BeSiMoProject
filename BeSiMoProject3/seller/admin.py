from django.contrib import admin
from .models import *
from django.utils.html import format_html
from store.models import Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category','description', 'seller', 'image_tag', 'stockqty']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.image.url))

    image_tag.short_description = 'Image'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class SellerAdmin(admin.ModelAdmin):
    list_display = ["store_name", "location"]

    def __str__(self):
        return self.store_name
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["customer", "order_id", "product_id", "product", "price", "quantity", "total_price", "status"]

    def customer(self, obj):
        return obj.order.customer.first_name
    customer.short_description = 'Customer'

    def status(self, obj):
        return obj.order.status
    status.short_description = 'Status'

    def product(self, obj):
        return obj.product.name
    product.short_description = 'Product'

    def total_price(self, obj):
        return obj.order.paid_amount
    total_price.short_description = 'Total Price'

# Register your models here.
admin.site.register(Seller, SellerAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OrderItem, OrderItemAdmin)



