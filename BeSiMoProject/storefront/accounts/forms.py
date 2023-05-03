from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Buyer
import re

class BuyerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput, label='Password confirmation')

    class Meta:
        model = Buyer
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
            'password_again': forms.PasswordInput,
        }

