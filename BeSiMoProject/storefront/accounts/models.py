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


