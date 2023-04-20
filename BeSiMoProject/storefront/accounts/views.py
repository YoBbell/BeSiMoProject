from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator, EmailValidator

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# def signup(self, request, user):
#     user.name = self.cleaned_data['name']
#     user.password = self.cleaned_data['password']
#     user.address = self.cleaned_data['address']
#     user.telephone_number = self.cleaned_data['telephone_number']
#     user.email = self.cleaned_data['email']
#     user.save()

