from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.contrib.auth.hashers import make_password,  check_password
from django.views import  View
from store.middlewares.auth import auth_middleware
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def cart(request):
    if request.method == "GET":
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products})
    elif request.method == "POST":
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('cart/')


# def cart(request):
#     if 'cart' in request.session:
#         ids = list(request.session.get('cart').keys())
#         products = Products.get_products_by_id(ids)
#     else:
#         products = []
#     return render(request, 'cart.html', {'products': products})


def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer_id, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer_id),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')

    return render(request)


def index(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    else:
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            products = Products.get_all_products()

        data = {}
        data['products'] = products
        data['categories'] = categories

        print('you are: ', request.session.get('email'))
        return render(request, 'index.html', data)







from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Customer


# def login_user(request):
#     error = None
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)

#             return redirect('edit_account/') # Change this to the correct URL for the edit account page
#         else:
#             error = 'Invalid email or password.'

#     return render(request, 'login.html', {'error': error})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_user(request):
    error = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            customer = Customer.objects.get(email=email)
            user = authenticate(request, username=customer.created_by.username, password=password)
        except Customer.DoesNotExist:
            user = None
            
        if user is not None:
            login(request, user)
            request.session['customer_id'] = customer.id
            return redirect('store/')
        else:
            error = 'Invalid email or password.'

    return render(request, 'login.html', {'error': error})










def logout(request):
    request.session.clear()
    return redirect('store')


def orders(request):
    customer = request.session.get('customer')
    orders = Order.get_orders_by_customer(customer)
    print(orders)
    return render(request, 'orders.html', {'orders': orders})


# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.core.validators import RegexValidator
# from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password
# from .models import Customer

# def signup(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Perform validation
#         error_message = None
#         if not first_name:
#             error_message = "Please enter your first name"
#         elif len(first_name) < 3:
#             error_message = "First name must be at least 3 characters long"
#         elif not last_name:
#             error_message = "Please enter your last name"
#         elif len(last_name) < 3:
#             error_message = "Last name must be at least 3 characters long"
#         elif not phone:
#             error_message = "Please enter your phone number"
#         elif not re.match(r'^(\+66|0)\d{9}$', phone):
#             error_message = "Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'"
#         elif not email:
#             error_message = "Please enter your email address"
#         elif not re.match(r'^\d{9,11}@student\.chula\.ac\.th$', email):
#             error_message = "Email must be in the format: 6xxxxxxxxx@student.chula.ac.th"
#         elif len(password) < 5:
#             error_message = "Password must be at least 5 characters long"
#         else:
#             try:
#                 # Create new user
#                 user = User.objects.create_user(username=email, password=password)
#                 user.first_name = first_name
#                 user.last_name = last_name
#                 user.save()

#                 # Create new customer
#                 customer = Customer(created_by=user, first_name=first_name, last_name=last_name, phone=phone, email=email, password=make_password(password))
#                 customer.save()

#                 return redirect('homepage')
#             except ValidationError as e:
#                 error_message = e.message

#         data = {
#             'error': error_message,
#             'values': request.POST
#         }
#         return render(request, 'signup.html', data)

#     return render(request, 'signup.html')

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.db import IntegrityError
from django.shortcuts import render, redirect

from django.utils.datastructures import MultiValueDictKeyError
from .models import Customer

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')


        try:
            password_confirm = request.POST['password_confirm']
        except MultiValueDictKeyError:
            error_message = 'Please confirm your password'
            data = {
                'error': error_message,
                'values': request.POST
            }
            return render(request, 'sell_signup.html', data)
        # Validate input
        error_message = None
        if not password_confirm:
            error_message = 'Please confirm your password'
        elif password != password_confirm:
            error_message = 'Passwords do not match'
        elif len(first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif len(last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif len(phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif not re.match(r'^(\+66|0)\d{9}$',phone):
            error_message ="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'"
        elif len(password) < 5:
            error_message = 'Password must be 5 char long'
        elif len(email) < 5:
            error_message = 'Email must be 5 char long'
        elif not re.match(r'^\d{10}\@student\.chula\.ac\.th$', email):
            error_message = 'Email must be in the format: xxxxxxxxxx@student.chula.ac.th'
        elif Customer.objects.filter(email=email).exists():
            error_message = 'Email Address Already Registered..'
        elif User.objects.filter(username=email).exists():
            error_message = 'Username (email) already exists.'
        else:
            # Create user
            user = User(username=email, password=make_password(password))
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Create customer
            customer = Customer.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    phone=phone,
                    email=email,
                    created_by=user )
            customer.save()

            return redirect('login')

        data = {
            'error': error_message,
            'values': request.POST
        }
        return render(request, 'signup.html', data)

    return render(request, 'signup.html')



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# @login_required(login_url='/login/')
# def edit_account(request):
#     user = request.user
#     customer = user.customer

#     if request.method == 'POST':
#         # Update customer information
#         customer.first_name = request.POST.get('first_name')
#         customer.last_name = request.POST.get('last_name')
#         customer.phone = request.POST.get('phone')
#         customer.email = request.POST.get('email')

#         # Update customer images

#         try:
#             customer.save() # save the updated customer information to the database
#             messages.success(request, 'Account updated successfully.')
#         except Exception as e:
#             messages.error(request, 'Failed to update account: {}'.format(e))

#     else:
#         if not request.user.is_authenticated:
#             return redirect('login/') # redirect the user to the login page if they are not authenticated

#     return render(request, 'edit_account.html', {'customer': request.user.customer})


@login_required(login_url='/login/')
def edit_account(request):
    user = request.user
    customer = user.customer

    if request.method == 'POST':
        # Update customer information
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        
        # Validate input
        error_message = None
        if len(customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif len(customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif not re.match(r'^(\+66|0)\d{9}$', customer.phone):
            error_message = "Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'"
        elif not re.match(r'^\d{10}\@student\.chula\.ac\.th$', customer.email):
            error_message = "Email must be in the format 'XXXXXXXXXX@student.chula.ac.th'"
        elif Customer.objects.filter(email=customer.email).exclude(id=customer.id).exists():
            error_message = 'Email Address Already Registered..'
            
        if error_message:
            messages.error(request, error_message)
        else:
            # Update customer images
            try:
                customer.save() # save the updated customer information to the database
                
                # update email of associated User object
                user.email = customer.email
                user.save()
                
                messages.success(request, 'Account updated successfully.')
            except Exception as e:
                messages.error(request, 'Failed to update account: {}'.format(e))

    return render(request, 'edit_account.html', {'customer': customer})





def start(request):
    return render(request, 'start.html')

def product_detail(request, id):
    product = Products.objects.get(id=id)
    return render(request, "product_detail.html", {"data": product})

def brand_list(request):
    data=Store.objects.all().order_by('-id')
    return render(request,'brand_list.html',{'data':data})

def brand_product_list(request,store_id):
	store=Store.objects.get(id=store_id)
	data=Products.objects.filter(store=store).order_by('-id')
	return render(request,'brand_product_list.html',{
			'data':data,
			})

# def auth_middleware(get_response):
#     def middleware(request):
#         if not request.session.get('customer_id'):
#             return redirect('cart/login/')
#         response = get_response(request)
#         return response
#     return middleware

