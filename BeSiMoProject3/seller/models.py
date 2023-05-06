from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User

class Seller(models.Model):
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE,)
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
