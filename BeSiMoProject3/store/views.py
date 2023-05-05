from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.contrib.auth.hashers import make_password,  check_password
from django.views import  View
from store.middlewares.auth import auth_middleware


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


def login(request):
    return_url = None
    if request.method == 'GET':
        return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return redirect('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')


def orders(request):
    customer = request.session.get('customer')
    orders = Order.get_orders_by_customer(customer)
    print(orders)
    return render(request, 'orders.html', {'orders': orders})


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # validation
        error_message = None
        if not first_name:
            error_message = "Please Enter your First Name !!"
        elif len(first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not last_name:
            error_message = 'Please Enter your Last Name'
        elif len(last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not phone:
            error_message = 'Enter your Phone Number'
        elif len(phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(password) < 5:
            error_message = 'Password must be 5 char long'
        elif len(email) < 5:
            error_message = 'Email must be 5 char long',
        elif not re.match(r'^\d{10}\@student\.chula\.ac\.th$', email):
            error_message = 'Email must be in the format: 6xxxxxxxxx@student.chula.ac.th'
        elif Customer.objects.filter(email=email).exists():
            error_message = 'Email Address Already Registered..'
        else:
            customer = Customer(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                password=make_password(password))
            customer.save()
            return redirect('homepage')

        data = {
            'error': error_message,
            'values': request.POST
        }
        return render(request, 'signup.html', data)

    return render(request, 'signup.html')


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
