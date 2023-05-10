from django.contrib import admin
from .models import *
from django.utils.html import format_html


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name

# Register your models here.
admin.site.register(Customer, CustomerAdmin)
# admin.site.register(Order)

