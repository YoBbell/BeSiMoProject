from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
import re

class Buyer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='First Name')
    last_name = models.CharField(max_length=100, verbose_name='Last Name')
    phone_regex = RegexValidator(
        regex=r'^(\+66|0)\d{9}$',
        message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
    phone = models.CharField(validators=[phone_regex], max_length=10)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    password_again = models.CharField(max_length=255, verbose_name='Password confirmation')

    def clean(self):
        if self.password != self.password_again:
            raise ValidationError('Passwords do not match')

        self.clean_email()

    def clean_email(self):
        email = self.email
        if not re.match(r'^\d{10}@student\.chula\.ac\.th$', email):
            raise ValidationError('Email must be a valid Chula email address')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=140, default='DEFAULT VALUE')
    price = models.FloatField()
    inventory = models.IntegerField(null=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    store = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


