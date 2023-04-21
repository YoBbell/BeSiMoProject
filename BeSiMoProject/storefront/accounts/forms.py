from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView

class SignupForm(forms.Form):
    fristname = forms.CharField(label='FristName', max_length=100, widget=forms.TextInput(attrs={'pattern': '[a-zA-Z ]+'}))
    lastname = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(attrs={'pattern': '[a-zA-Z ]+'}))
    phone_regex = RegexValidator(
        regex=r'^(\+66|0)\d{9}$',
        message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
    phone = forms.CharField(validators=[phone_regex])
    email = forms.CharField(validators=[EmailValidator(message='Email must be a valid Chula email address')])
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())
    password_again = forms.CharField(max_length=255,label='Password confirmation', widget=forms.PasswordInput(), error_messages={'required': 'Please confirm your password', 'invalid': 'Passwords do not match'})

    # clean_password แต่ต้องใช้ชื่อ clean เพราะเป็น function ใช้คู่กับ clean()
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')
        if password and password_again and password != password_again:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
    

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@student.chula.ac.th'):
            raise forms.ValidationError('Email must be a valid Chula email address')
        return email
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class SuccessView(TemplateView):
    template_name = 'success.html'

