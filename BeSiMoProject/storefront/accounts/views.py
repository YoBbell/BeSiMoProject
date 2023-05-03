from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import BuyerForm
from .models import Category, Product

def signup(request):
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('success')
    else:
        form = BuyerForm()
    return render(request, 'signup.html', {'form': form})



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

# def product_browse(request):
#     products = Product.objects.all()
#     print(f"products items: {products}")
#     return render(request, 'product_browse.html' ,{'products': products})

def product_browse(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(collection=category).order_by('-last_update')
    return render(request, 'product_browse.html', {'category': category, 'products': products})
