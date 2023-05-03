from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import BuyerForm
from .models import Category

# def signup(request):
#     if request.method == 'POST':
#         form = BuyerForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('success')
#     else:
#         form = BuyerForm()
#     return render(request, 'signup.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = BuyerForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('success')
#         else:
#             if form.cleaned_data.get('password') != form.cleaned_data.get('password_again'):
#                 form.add_error('password_again', 'Passwords do not match')
#     else:
#         form = BuyerForm()
#     return render(request, 'signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('password') != form.cleaned_data.get('password_again'):
                form.add_error('password_again', 'Passwords do not match')
            else:
                user = form.save()
                login(request, user)
                return redirect('success')
    else:
        form = BuyerForm()
    return render(request, 'signup.html', {'form': form})

def register(request):
    return render(request, "register.html")


def success(request):
    return render(request, 'success.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def category_browse(request):
    categories = Category.objects.all()
    print(f"category items: {categories}")
    return render(request, 'category_browse.html' ,{'categories': categories})

