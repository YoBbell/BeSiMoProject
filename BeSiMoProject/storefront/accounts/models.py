from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator


class Buyer(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)   
    # telephone_number = models.CharField(
    #     max_length=17, 
    #     validators=[
    #         RegexValidator(
    #             regex=r'^\+?1?\d{9,15}$',
    #             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    #         )
    #     ]
    # )
    # email = models.EmailField(validators=[EmailValidator()])


    def __str__(self):
        return self.name


# class Buyer(forms.Form):
#     name = forms.CharField(max_length=255)
#     password = forms.CharField(widget=forms.PasswordInput)
#     address = forms.CharField(max_length=255)
#     telephone_number = forms.CharField(max_length=17, validators=[RegexValidator(
#             regex=r'^\+?1?\d{9,15}$',
#             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
#         )])
#     email = forms.EmailField(validators=[EmailValidator()])


