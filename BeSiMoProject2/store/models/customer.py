from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


# class Customer(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField (max_length=50)
#     phone = models.CharField(max_length=10)
#     email=models.EmailField()
#     password = models.CharField(max_length=100)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    
    phone_regex = RegexValidator(
        regex=r'^(\+66|0)\d{9}$',
        message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
    phone = models.CharField(validators=[phone_regex], max_length=10)
    
    email_regex = re.compile(r'^\d{9,11}@student\.chula\.ac\.th$')
    email = models.EmailField(unique=True)

    def clean(self):
        if not self.email_regex.match(self.email):
            raise ValidationError({'email': 'Email must be in the format: \'xxxxxxxxxx@student.chula.ac.th\''})

        if not validate_email(self.email):
            raise ValidationError({'email': 'Please enter a valid email address'})

    # email_regex = RegexValidator(
    #     regex=r'^\d{9,11}@student.chula.ac.th$',
    #     message="Email must be in the format: '6xxxxxxxxx@student.chula.ac.th'")
    # email = models.EmailField(validators=[email_regex], unique=True, error_messages={'invalid': 'Please enter a valid email address'})

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