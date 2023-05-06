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


def cart(request):
    if 'cart' in request.session:
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
    else:
        products = []
    return render(request, 'cart.html', {'products': products})


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
            return redirect('edit_account')
        else:
            error = 'Invalid email or password.'

    return render(request, 'login.html', {'error': error})










def logout(request):
    request.session.clear()
    return redirect('start')


def orders(request):
    customer = request.session.get('customer')
    orders = Order.get_orders_by_customer(customer)
    print(orders)
    return render(request, 'orders.html', {'orders': orders})


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        phone = request.POST['phone']
        email = request.POST['email']
       

        # create a new user
        user = User.objects.create_user(username=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # create a new customer
        customer = Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            password=password,
            phone=phone,
            email=email,
            created_by=user
        )
        customer.save()

        messages.success(request, 'Your account has been created successfully!')
        return redirect('login')

    return render(request, 'signup.html')

# def signup(request):
#     if request.method == 'POST':
#         user = request.user
#         first_name = request.POST.get('firstname')
#         last_name = request.POST.get('lastname')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # validation
#         error_message = None
#         if not first_name:
#             error_message = "Please Enter your First Name !!"
#         elif len(first_name) < 3:
#             error_message = 'First Name must be 3 char long or more'
#         elif not last_name:
#             error_message = 'Please Enter your Last Name'
#         elif len(last_name) < 3:
#             error_message = 'Last Name must be 3 char long or more'
#         elif not phone:
#             error_message = 'Enter your Phone Number'
#         elif len(phone) < 10:
#             error_message = 'Phone Number must be 10 char Long'
#         elif len(password) < 5:
#             error_message = 'Password must be 5 char long'
#         elif len(email) < 5:
#             error_message = 'Email must be 5 char long',
#         elif not re.match(r'^\d{10}\@student\.chula\.ac\.th$', email):
#             error_message = 'Email must be in the format: 6xxxxxxxxx@student.chula.ac.th'
#         elif Customer.objects.filter(email=email).exists():
#             error_message = 'Email Address Already Registered..'
#         else:
#             customer = Customer(created_by=user,
#                                 first_name=first_name,
#                                 last_name=last_name,
#                                 phone=phone,
#                                 email=email,
#                                 password=make_password(password))
#             customer.save()
#             return redirect('homepage')

#         data = {
#             'error': error_message,
#             'values': request.POST
#         }
#         return render(request, 'signup.html', data)

#     return render(request, 'signup.html')


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

        # Update customer images

        try:
            customer.save() # save the updated customer information to the database
            
            # update email of associated User object
            user.email = request.POST.get('email')
            user.save()
            
            messages.success(request, 'Account updated successfully.')
        except Exception as e:
            messages.error(request, 'Failed to update account: {}'.format(e))

    return render(request, 'edit_account.html', {'customer': request.user.customer})



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
