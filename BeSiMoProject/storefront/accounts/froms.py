from django import forms
from .models import Customer
from django.contrib.auth.hashers import make_password

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 10:
            raise forms.ValidationError('Phone Number must be 10 char Long')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) < 5:
            raise forms.ValidationError('Email must be 5 char long')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Address Already Registered..')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5:
            raise forms.ValidationError('Password must be 5 char long')
        return make_password(password)
