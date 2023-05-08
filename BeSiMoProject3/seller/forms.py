from django.forms import ModelForm, models

from .models import *
from django import forms


class ProductForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    
    class Meta:
        model = Products
        fields = [ 'category','name', 'price', 'image', 'stockqty']


#----------------------------------------
from django import forms
from django.forms.fields import IntegerField
from django.forms.forms import Form


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()