from django.forms import ModelForm, models

from .models import Item


class ProductForm(ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'image', 'title', 'description', 'price']

#----------------------------------------
from django import forms
from django.forms.fields import IntegerField
from django.forms.forms import Form


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()