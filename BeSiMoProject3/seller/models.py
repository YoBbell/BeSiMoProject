from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
import datetime

class Seller(models.Model):
    created_by = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    store_name = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100)
    
    phone_regex = RegexValidator(
        regex=r'^(\+66|0)\d{9}$',
        message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
    phone = models.CharField(validators=[phone_regex], max_length=12)
    
    email_regex = re.compile(r'^\d{9,11}@student\.chula\.ac\.th$')
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=250, default='')
    store_image= models.ImageField(upload_to='uploads/seller_data/')
    qr_image= models.ImageField(upload_to='uploads/seller_data/')
    

    def clean(self):
        if not self.email_regex.match(self.email):
            raise ValidationError({'email': 'Email must be in the format: \'xxxxxxxxxx@student.chula.ac.th\''})

  
    def register(self):
        self.save()


    @staticmethod
    def get_seller_by_email(email):
        try:
            return Seller.objects.get(email= email)
        except:
            return False


    def isExists(self):
        if Seller.objects.filter(email = self.email):
            return True

        return False
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def __str__(self):
        return self.store_name


class Category(models.Model):
    name= models.CharField(max_length=50)
    cat_image= models.ImageField(upload_to='uploads/categories/')

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name



class Products(models.Model):
    name = models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    category= models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,default=1 )
    description= models.CharField(max_length=250, default='', blank=True, null= True)
    seller = models.ForeignKey(Seller, related_name='products', on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    image= models.ImageField(upload_to='uploads/products/')
    stockqty = models.IntegerField(default=999)

    class Meta:
        ordering = ['-added_date']

    @staticmethod
    def get_products_by_id(ids):
        if ids:
            return Products.objects.filter(id__in=ids)
        else:
            return []

    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter (category=category_id)
        else:
            return Products.get_all_products();
            
    def __str__(self):
        return self.name
    
class Payment(models.Model):
    receipt = models.ImageField(upload_to='uploads/payment/')

    def __str__(self):
        return str(self.id)
    
from store.models import *
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name="items", on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return self.price * self.quantity

    @staticmethod
    def get_orderitem_by_order(order_id):
        return OrderItem.objects.filter(order=order_id)


    
# class Item(models.Model):
#     title = models.CharField(max_length=50)
#     category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
#     seller = models.ForeignKey(Seller, related_name="items", on_delete=models.CASCADE)
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     added_date = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(upload_to='uploads/', blank=True, null=True)
#     thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Change uploads to thumbnails 

#     class Meta:
#         ordering = ['-added_date']

#     def __str__(self):
#         return self.title

#     # ordering = models.IntegerField(default=0)

#     # class Meta:
#     #     ordering = ['ordering']
# #-----------------------------------------------


# # class Products(models.Model):
# #     name = models.CharField(max_length=60)
# #     price= models.IntegerField(default=0)
# #     category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1 )
# #     description= models.CharField(max_length=250, default='', blank=True, null= True)
# #     store = models.ForeignKey(Seller,on_delete=models.CASCADE)
# #     location = models.CharField(max_length=250, default='')
# #     image= models.ImageField(upload_to='uploads/products/')

# #     @staticmethod
# #     def get_products_by_id(ids):
# #         return Products.objects.filter (id__in=ids)
# #     @staticmethod
# #     def get_all_products():
# #         return Products.objects.all()

# #     @staticmethod
# #     def get_all_products_by_categoryid(category_id):
# #         if category_id:
# #             return Products.objects.filter (category=category_id)
# #         else:
# #             return Products.get_all_products();

# from store.models import Customer
# class Order(models.Model):
#     PENDING = 'pending'
#     COMPLETED = 'completed'
#     CANCELLED = 'cancelled'
#     STATUS_CHOICES = [
#         (PENDING, 'Pending'),
#         (COMPLETED, 'Completed'),
#         (CANCELLED, 'Cancelled'),
#     ]


#     product = models.ForeignKey(Products,
#                                 on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer,
#                                  on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.IntegerField()
#     address = models.CharField (max_length=50, default='', blank=True)
#     phone = models.CharField (max_length=50, default='', blank=True)
#     date = models.DateField (default=datetime.datetime.today)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

#     def placeOrder(self):
#         self.save()

#     @staticmethod
#     def get_orders_by_customer(customer_id):
#         return Order.objects.filter(customer=customer_id).order_by('-date')
