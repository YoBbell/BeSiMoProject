from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
import datetime

class Category(models.Model):
    name= models.CharField(max_length=50)
    cat_image= models.ImageField(upload_to='uploads/categories/')

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    created_by = models.OneToOneField(User, related_name='buyer', on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    
    phone_regex = RegexValidator(
        regex=r'^(\+66|0)\d{9}$',
        message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
    phone = models.CharField(validators=[phone_regex], max_length=12)
    
    email_regex = re.compile(r'^\d{9,11}@student\.chula\.ac\.th$')
    email = models.EmailField(unique=True)
    

    def clean(self):
        if not self.email_regex.match(self.email):
            raise ValidationError({'email': 'Email must be in the format: \'xxxxxxxxxx@student.chula.ac.th\''})

  
    def register(self):
        self.save()


    @staticmethod
    def get_seller_by_email(email):
        try:
            return Customer.objects.get(email= email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    
# class Customer(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField (max_length=50)
#     phone = models.CharField(max_length=10)
#     email=models.EmailField()
#     password = models.CharField(max_length=100)

# class Customer(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     password = models.CharField(max_length=100)
    
#     phone_regex = RegexValidator(
#         regex=r'^(\+66|0)\d{9}$',
#         message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
#     phone = models.CharField(validators=[phone_regex], max_length=10)
    
#     email_regex = re.compile(r'^\d{9,11}@student\.chula\.ac\.th$')
#     email = models.EmailField(unique=True)

#     def clean(self):
#         if not self.email_regex.match(self.email):
#             raise ValidationError({'email': 'Email must be in the format: \'xxxxxxxxxx@student.chula.ac.th\''})

#         # if not validate_email(self.email):
#         #     raise ValidationError({'email': 'Please enter a valid email address'})

#     # email_regex = RegexValidator(
#     #     regex=r'^\d{9,11}@student.chula.ac.th$',
#     #     message="Email must be in the format: '6xxxxxxxxx@student.chula.ac.th'")
#     # email = models.EmailField(validators=[email_regex], unique=True, error_messages={'invalid': 'Please enter a valid email address'})

#     #to save the data
#     def register(self):
#         self.save()


#     @staticmethod
#     def get_customer_by_email(email):
#         try:
#             return Customer.objects.get(email= email)
#         except:
#             return False


#     def isExists(self):
#         if Customer.objects.filter(email = self.email):
#             return True

#         return False
    
#     def __str__(self):
#         return self.first_name + " " + self.last_name
    
class Store(models.Model):
    store_name = models.CharField(max_length=100, default='')    
    phone_regex = RegexValidator(
        regex=r'^(\+66|0)\d{9}$',
        message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
    phone = models.CharField(validators=[phone_regex], max_length=12)
    
    email_regex = re.compile(r'^\d{9,11}@student\.chula\.ac\.th$')
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=250, default='')
    store_image= models.ImageField(upload_to='uploads/store_data/')
    qr_image= models.ImageField(upload_to='uploads/store_data/')

    def __str__(self):
        return self.store_name


class Products(models.Model):
    name = models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1 )
    description= models.CharField(max_length=250, default='', blank=True, null= True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    location = models.CharField(max_length=250, default='')
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
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
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
    
