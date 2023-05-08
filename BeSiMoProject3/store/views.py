from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
import json
from seller.models import *
from store.models import *
import datetime
from django.contrib.auth.hashers import make_password,  check_password
from django.views import  View
from store.middlewares.auth import auth_middleware
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError


@login_required(login_url='/login/')
def cart(request):
    print(f"is_authen: {request.user.is_authenticated}")
    # if request.method == "GET":
    #     ids = list(request.session.get('cart', {}).keys())
    #     products = Products.get_products_by_id(ids)
    #     return render(request, 'cart.html', {'products': products})
    if request.method == 'GET':
        id = request.session.get('cart').keys()
        products = []
        if id:
            id = [int(pdid) for pdid in id]
            products = Products.get_products_by_id(id)
        return render(request, 'cart.html', {'products': products})
    # if request.method == 'GET':
    #     ids = request.session.get('cart').keys()
    #     if ids:
    #         products = Products.get_products_by_id(ids)
    #     else:
    #         products = []
    #         return render(request, 'cart.html', {'products': products})
    elif request.method == "POST":
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})

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

# @login_required(login_url='/login/')
# def checkout(request):
#     if request.method == 'POST':
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         customer_id = request.session.get('customer_id')
#         cart = request.session.get('cart')
#         products = Products.get_products_by_id(list(cart.keys()))

#         try:
#             customer = Customer.objects.get(id=customer_id)
#         except Customer.DoesNotExist:
#             return redirect('orders')

#         order = Order.objects.create(customer=customer, paid_amount=0)

#         for product in products:
#             order_item = OrderItem.objects.create(order=order,
#                                                   product=product,
#                                                   price=product.price,
#                                                   quantity=cart.get(str(product.id)))
#         order.paid_amount = OrderItem.get_total_price(order_item)
#         order.save()
#         request.session['cart'] = {}

#         return redirect('orders')

#     cart = request.session.get('cart')
#     if not cart:
#         return redirect('cart')

#     products = Products.get_products_by_id(list(cart.keys()))
#     return render(request, 'checkout.html', {'products': products})


# def checkout(request):
#     if request.method == 'POST':
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         customer_id = request.session.get('customer_id')
#         cart = request.session.get('cart')
#         products = Products.get_products_by_id(list(cart.keys()))
#         print(address, phone, customer_id, cart, products)

#         for product in products:
#             print(cart.get(str(product.id)))
#             order = Order(customer=Customer(id=customer_id),
#                           product=product,
#                           price=product.price,
#                           address=address,
#                           phone=phone,
#                           quantity=cart.get(str(product.id)))
#             order.save()
#         request.session['cart'] = {}

#         return redirect('cart')
#     return render(request, 'checkout.html')



# def checkout(request):
#     if request.method == 'POST':
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         customer_id = request.session.get('customer_id')
#         cart = request.session.get('cart')
#         products = Products.get_products_by_id(list(cart.keys()))

#         try:
#             customer = Customer.objects.get(id=customer_id)
#         except Customer.DoesNotExist:
#             return redirect('orders')

#         order = Order.objects.create(customer=customer, paid_amount=0)

#         for product in products:
#             order_item = OrderItem.objects.create(order=order,
#                                                   product=product,
#                                                   price=product.price,
#                                                   quantity=cart.get(str(product.id)))
#         order.paid_amount = cart.get_total_price()
#         order.save()
#         request.session['cart'] = {}

#         return redirect('orders')

#     return render(request, 'checkout.html')

def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        customer = Customer.objects.get(id=customer_id)
        print(address, phone, customer_id, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order.objects.create(
                customer=customer,
                paid_amount=product.price,
                status=Order.PENDING,
            )
            order.save()
            
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=cart.get(str(product.id)),
            )
            order_item.save()
            
        request.session['cart'] = {}

        return redirect('orders')

    return render(request, 'checkout.html')

# def checkout(request):
#     if request.method == 'POST':
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         customer_id = request.session.get('customer_id')
#         cart = request.session.get('cart')
#         products = Products.get_products_by_id(list(cart.keys()))

#         try:
#             customer = Customer.objects.get(id=customer_id)
#         except Customer.DoesNotExist:
#             return redirect('orders')

#         order = Order.objects.create(customer=customer, paid_amount=0)

#         for product in products:
#             order_item = OrderItem.objects.create(order=order,
#                                                   product=product,
#                                                   price=product.price,
#                                                   quantity=cart.get(str(product.id)))
#         # order.paid_amount = order.get_total_price()
#         order.save()
#         request.session['cart'] = {}

#         context = {'cart': cart} # Add cart data to context dictionary
#         return render(request, 'orders.html', context)

#     return render(request, 'checkout.html')


# def checkout(request):
#     if request.method == 'POST':
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         customer = request.session.get('customer')
#         cart = request.session.get('cart')
#         products = Products.get_products_by_id(list(cart.keys()))
#         print(address, phone, customer, cart, products)

#         for product in products:
#             print(cart.get(str(product.id)))
#             order = Order(customer=Customer(id=customer),
#                         product=product,
#                         price=product.price,
#                         address=address,
#                         phone=phone,
#                         quantity=cart.get(str(product.id)))
#             order.save()
#         request.session['cart'] = {}

#         return redirect('cart')

# def checkout(request):
#     if request.method == 'POST':
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         customer_id = request.session.get('customer')
#         cart = request.session.get('cart')
#         products = Products.get_products_by_id(list(cart.keys()))
#         print(address, phone, customer_id, cart, products)

#         for product in products:
#             print(cart.get(str(product.id)))
#             order = Order(customer=Customer(id=customer_id),
#                           product=product,
#                           price=product.price,
#                           address=address,
#                           phone=phone,
#                           quantity=cart.get(str(product.id)))
#             order.save()
#         request.session['cart'] = {}

#         return redirect('cart')

#     return render(request)

# def checkout(request):
#     if request.method == 'POST':
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         customer_id = request.session.get('customer')
#         cart = request.session.get('cart')
#         products = Products.get_products_by_id(list(cart.keys()))
#         print(address, phone, customer_id, cart, products)

#         # try:
#         #     customer = Customer.objects.get(id=customer_id)
#         # except Customer.DoesNotExist:
#         #     return HttpResponse("Error: Customer not found")
        
#         customer = get_object_or_404(Customer, id=customer_id)
#         order = Order(customer=customer, paid_amount=0, status=Order.PENDING)
#         order.save()
        ## Create an Order instance for the customer
        # order = Order.objects.create(
        #     customer=Customer(id=customer_id),
        #     paid_amount=0,
        #     status=Order.PENDING,
        # )

        ## Create an OrderItem instance for each product in the cart
        # for product in products:
        #     quantity = cart.get(str(product.id))
        #     price = product.price
        #     OrderItem.objects.create(
        #         order=order,
        #         product=product,
        #         price=price,
        #         quantity=quantity,
        #     )

    #     for product in products:
    #         order_item = OrderItem(
    #             order=order,
    #             product=product,
    #             price=product.price,
    #             quantity=cart.get(str(product.id))
    #         )
    #         order_item.save()
    #         order.paid_amount += order_item.get_total_price()
    #     order.save()

    #     request.session['cart'] = {}

    #     return redirect('cart')

    # return render(request)



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


def save_review(request, id):
    print('hello')
    return render(request, 'index.html')




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
    customer_id = request.session.get('customer_id')
    orders = Order.get_orders_by_customer(customer_id)
    # orderitem = OrderItem.get_orderitem_by_order(orders.id)
    # print(orderitem)
    orderitems = []
    for order in orders:
        orderitems += OrderItem.objects.filter(order=order.id)
    print(orderitems)
    return render(request, 'orders.html', {'orderitems': orderitems})


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get("address")
        zipcode = request.POST.get("zipcode")


        try:
            password_confirm = request.POST['password_confirm']
        except MultiValueDictKeyError:
            error_message = 'Please confirm your password'
            data = {
                'error': error_message,
                'values': request.POST
            }
            return render(request, 'signup.html', data)
        
        # Validate input
        error_message = None
        if not password_confirm:
            error_message = 'Please confirm your password'
        elif password != password_confirm:
            error_message = 'Passwords do not match'
        if len(first_name) < 3:
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
                    address=address,
                    zipcode=zipcode,
                    created_by=user )
            customer.save()

            return redirect('login')

        data = {
            'error': error_message,
            'values': request.POST
        }
        return render(request, 'signup.html', data)

    return render(request, 'signup.html')



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
        customer.address = request.POST.get('address')
        customer.zipcode = request.POST.get('zipcode')
        

        
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
    data=Seller.objects.all().order_by('-id')
    return render(request,'brand_list.html',{'data':data})

def brand_product_list(request,seller_id):
	seller=Seller.objects.get(id=seller_id)
	data=Products.objects.filter(seller=seller).order_by('-id')
	return render(request,'brand_product_list.html',{
			'data':data,
			})



def buyer_payment(request, orderitem_id):
    # Get the current order item
    orderitem = OrderItem.objects.get(pk=orderitem_id)
    customer = orderitem.order.customer

    if request.method == 'POST':
        # Process payment and create Payment object
        receipt = request.FILES.get('receipt')
        if not receipt:
            messages.error(request, 'Please upload a payment receipt')
            return redirect('buyer_payment', orderitem_id=orderitem_id)
        payment = Payment.objects.create(orderitem=orderitem, receipt=receipt)


        # Get address and zipcode from the form data
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')

        # Validate that the address field is not empty
        if not address:
            messages.error(request, 'Please enter a valid address')
            return redirect('buyer_payment', orderitem_id=orderitem_id)

        # Set the address and zipcode on the order
        orderitem.order.address = address
        orderitem.order.zipcode = zipcode


        # Update order status to completed
        orderitem.order.status = Order.IN_PROCESS
        orderitem.order.save()


        messages.success(request, 'Payment confirmed. Thank you for your purchase!')
        return redirect('homepage')

    # Render template with seller, customer, and order info
    context = {
        'seller_name': orderitem.product.seller.store_name,
        'seller_location': orderitem.product.seller.location,
        'seller_qr_image': orderitem.product.seller.qr_image,

        'customer_first_name': customer.first_name,
        'customer_last_name': customer.last_name,
        'customer_phone': customer.phone,
        'customer_address' : customer.address,
        'customer_zipcode' : customer.zipcode,

        'order_item_product_name': orderitem.product.name,
        'order_item_quantity': orderitem.quantity,
        'order_item_price': orderitem.product.price,
        'order_item_total_price': orderitem.get_total_price()
        
    }
    return render(request, 'buyer_payment.html', context)


def receipt(request, orderitem_id):

    orderitem = OrderItem.objects.get(pk=orderitem_id)
    customer = orderitem.order.customer

    context = {
        'seller_name': orderitem.product.seller.store_name,
        'seller_location': orderitem.product.seller.location,
        

        'customer_first_name': customer.first_name,
        'customer_last_name': customer.last_name,
        'customer_phone': customer.phone,

        'order_address' : orderitem.order.address,
        'order_zipcode' : orderitem.order.zipcode,
        
        'payment_img' : orderitem.payment.receipt,
        

        'order_item_product_name': orderitem.product.name,
        'order_item_quantity': orderitem.quantity,
        'order_item_price': orderitem.product.price,
        'order_item_total_price': orderitem.get_total_price()
        
    }

    return render(request, 'receipt.html', context)



# def auth_middleware(get_response):
#     def middleware(request):
#         if not request.session.get('customer_id'):
#             return redirect('cart/login/')
#         response = get_response(request)
#         return response
#     return middleware


# def login_user(request):
#     return_url = None
#     # error = None
#     if request.method == 'GET':
#         return_url = request.GET.get('return_url')
#         return render(request, 'login.html')

#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         try:
#             customer = Customer.objects.get(email=email)
#             user = authenticate(request, username=customer.created_by.username, password=password)
#         except Customer.DoesNotExist:
#             user = None
            
#         if user is not None:
#             login(request, user)
#             request.session['customer_id'] = customer.id
#             return redirect('store/')
#         else:
#             error = 'Invalid email or password.'

#     return render(request, 'login.html', {'error': error})


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


# def cart(request):
#     if 'cart' in request.session:
#         ids = list(request.session.get('cart').keys())
#         products = Products.get_products_by_id(ids)
#     else:
#         products = []
#     return render(request, 'cart.html', {'products': products})