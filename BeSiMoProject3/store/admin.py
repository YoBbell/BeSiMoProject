from django.contrib import admin
from seller.models import Products, Category, Customer, Order, Seller
from django.utils.html import format_html

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'price', 'category', 'location', 'image_tag']

#     def image_tag(self, obj):
#         return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.image.url))

    # image_tag.short_description = 'Image'

    # def store_name(self, obj):
    #     return obj.seller


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'cat_image_tag']

#     def __str__(self):
#         return self.name

#     def cat_image_tag(self, obj):
#         return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.cat_image.url))

#     cat_image_tag.short_description = 'Image'

# class SellerAdmin(admin.ModelAdmin):
#     list_display = ["store_name", "location"]

    # def __str__(self):
    #     return self.store_name

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name

# Register your models here.
# admin.site.register(Products, ProductAdmin)
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
# admin.site.register(Order)
# admin.site.register(Seller, SellerAdmin)
