from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
import re
import datetime

# class Buyer(models.Model):
#     first_name = models.CharField(max_length=100, verbose_name='First Name')
#     last_name = models.CharField(max_length=100, verbose_name='Last Name')
#     phone_regex = RegexValidator(
#         regex=r'^(\+66|0)\d{9}$',
#         message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
#     phone = models.CharField(validators=[phone_regex], max_length=10)
#     email = models.CharField(max_length=100)
#     password = models.CharField(max_length=255)
#     password_again = models.CharField(max_length=255, verbose_name='Password confirmation')

#     def clean(self):
#         if self.password != self.password_again:
#             raise ValidationError('Passwords do not match')

#         self.clean_email()

#     def clean_email(self):
#         email = self.email
#         if not re.match(r'^\d{10}@student\.chula\.ac\.th$', email):
#             raise ValidationError('Email must be a valid Chula email address')

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='images/')
    
#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(max_length=140, default='DEFAULT VALUE')
#     price = models.FloatField()
#     inventory = models.IntegerField(null=True)
#     digital = models.BooleanField(default=False, null=True, blank=True)
#     last_update = models.DateTimeField(auto_now=True)
#     collection = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
#     location = models.CharField(max_length=200, null=True, blank=True)
#     image = models.ImageField(null=True, blank=True)

#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     image = models.ImageField(upload_to='product_images')
#     store = models.CharField(max_length=200)
#     location = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name
    
#     @property
#     def imageURL(self):
#         try:
#             url = self.image.url
#         except:
#             url = ''
#         return url


# from .models import Products
# from .models import Category
# from  .models import  Customer
# from  .models import  Order

# from django.db import models

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
import re

class Category(models.Model):
    name= models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField (max_length=50)
    phone = models.CharField(max_length=10)
    email=models.EmailField()
    password = models.CharField(max_length=100)

    #to save the data
    def register(self):
        self.save()


    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email= email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False


class Products(models.Model):
    name = models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1 )
    description= models.CharField(max_length=250, default='', blank=True, null= True)
    image= models.ImageField(upload_to='uploads/products/')

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter (id__in=ids)

    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter (category=category_id)
        else:
            return Products.get_all_products();


class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField (max_length=50, default='', blank=True)
    phone = models.CharField (max_length=50, default='', blank=True)
    date = models.DateField (default=datetime.datetime.today)
    status = models.BooleanField (default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
