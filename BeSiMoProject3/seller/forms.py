from django.forms import ModelForm, models

from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = [ 'category','name', 'description', 'price', 'image', 'stockqty']

#----------------------------------------
from django import forms
from django.forms.fields import IntegerField
from django.forms.forms import Form


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()