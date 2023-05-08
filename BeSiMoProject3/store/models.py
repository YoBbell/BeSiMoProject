from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
import datetime



class Customer(models.Model):
    created_by = models.OneToOneField(User, related_name='customer', on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=5)
    
    phone_regex = RegexValidator(
        regex=r'^(\+66|0)\d{9}$',
        message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
    phone = models.CharField(validators=[phone_regex], max_length=12)
    
    email_regex = re.compile(r'^\d{9,11}@student\.chula\.ac\.th$')
    email = models.EmailField(unique=True)

    def clean(self):
        if not self.email_regex.match(self.email):
            raise ValidationError({'email': 'Email must be in the format: \'6xxxxxxxxx@student.chula.ac.th\''})

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
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    # @staticmethod
    # def create_customer_for_user(user):
    #     customer = Customer(created_by=user)
    #     customer.save()
    #     return customer



class Order(models.Model):
    PENDING = 'pending'
    IN_PROCESS = 'in_process'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROCESS, 'In_process'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=5, default='')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    # seller = models.ForeignKey(Seller, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-created_at')

  
    def __str__(self):
        return self.customer.first_name
    




    

# class Payment(models.Model):
#     seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
#     receipt = models.ImageField(upload_to='uploads/payment/')

#     def __str__(self):
#         return str(self.id)


# class Category(models.Model):
#     name= models.CharField(max_length=50)
#     cat_image= models.ImageField(upload_to='uploads/categories/')

#     @staticmethod
#     def get_all_categories():
#         return Category.objects.all()

#     def __str__(self):
#         return self.name

    
# class Store(models.Model):
#     store_name = models.CharField(max_length=100, default='')    
#     phone_regex = RegexValidator(
#         regex=r'^(\+66|0)\d{9}$',
#         message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
#     phone = models.CharField(validators=[phone_regex], max_length=12)
    
#     email_regex = re.compile(r'^\d{9,11}@student\.chula\.ac\.th$')
#     email = models.EmailField(unique=True)
#     location = models.CharField(max_length=250, default='')
#     store_image= models.ImageField(upload_to='uploads/store_data/')
#     qr_image= models.ImageField(upload_to='uploads/store_data/')

#     def __str__(self):
#         return self.store_name


# class Products(models.Model):
#     name = models.CharField(max_length=60)
#     price= models.IntegerField(default=0)
#     category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1 )
#     description= models.CharField(max_length=250, default='', blank=True, null= True)
#     store = models.ForeignKey(Store,on_delete=models.CASCADE)
#     location = models.CharField(max_length=250, default='')
#     image= models.ImageField(upload_to='uploads/products/')

#     @staticmethod
#     def get_products_by_id(ids):
#         return Products.objects.filter (id__in=ids)
#     @staticmethod
#     def get_all_products():
#         return Products.objects.all()

#     @staticmethod
#     def get_all_products_by_categoryid(category_id):
#         if category_id:
#             return Products.objects.filter (category=category_id)
#         else:
#             return Products.get_all_products();


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
    
