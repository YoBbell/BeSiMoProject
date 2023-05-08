from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.hashers import make_password,  check_password
from seller.models import *
from django.views import View
import re
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm
from django.utils.text import slugify
from .models import Products




# def sell_signup(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         store_name = request.POST['store_name']
#         password = request.POST['password']
#         phone = request.POST['phone']
#         email = request.POST['email']
#         location = request.POST['location']
#         store_image = request.FILES['store_image']
#         qr_image = request.FILES['qr_image']

#         # Validate input
#         error_message = None
#         if  first_name is None:
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
#         elif not re.match(r'^(\+66|0)\d{9}$',phone):
#             error_message ="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'"
#         elif len(password) < 5:
#             error_message = 'Password must be 5 char long'
#         elif len(email) < 5:
#             error_message = 'Email must be 5 char long'
#         elif not re.match(r'^\d{10}\@student\.chula\.ac\.th$', email):
#             error_message = 'Email must be in the format: xxxxxxxxxx@student.chula.ac.th'
#         elif Seller.objects.filter(email=email).exists():
#             error_message = 'Email Address Already Registered..'
#         elif User.objects.filter(username=email).exists():
#             error_message = 'Username (email) already exists.'
#         else:
#             # Create user
#             user = User(username=email, password=make_password(password))
#             user.first_name = first_name
#             user.last_name = last_name
#             user.save()

#             # Create customer
#             seller = Seller.objects.create(
#                     first_name=first_name,
#                     last_name=last_name,
#                     store_name=store_name,
#                     password=password,
#                     phone=phone,
#                     email=email,
#                     location=location,
#                     store_image=store_image,
#                     qr_image=qr_image,
#                     created_by=user )
        
#             seller.save()

#             return redirect('sell_login')

#         data = {
#             'error': error_message,
#             'values': request.POST
#         }
#         return render(request, 'sell_signup.html', data)

#     return render(request, 'sell_signup.html')


from django.utils.datastructures import MultiValueDictKeyError

def sell_signup(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        store_name = request.POST['store_name']
        password = request.POST['password']
        phone = request.POST['phone']
        email = request.POST['email']
        location = request.POST['location']
        store_image = request.FILES['store_image']
        qr_image = request.FILES['qr_image']

        # Get password confirmation
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
        elif Seller.objects.filter(email=email).exists():
            error_message = 'Email Address Already Registered..'
        elif User.objects.filter(username=email).exists():
            error_message = 'Username (email) already exists.'
        else:
            # Create user
            user = User(username=email, password=make_password(password))
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Create seller
            seller = Seller.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    store_name=store_name,
                    password=password,
                    phone=phone,
                    email=email,
                    location=location,
                    store_image=store_image,
                    qr_image=qr_image,
                    created_by=user )
            seller.save()

            return redirect('sell_login')

        data = {
            'error': error_message,
            'values': request.POST
        }
        return render(request, 'sell_signup.html', data)

    return render(request, 'sell_signup.html')





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def sell_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('seller_admin') # เดี๋ยวมาเชื่อมอีกที
        else:
            error = 'Invalid email or password.'
        
    return render(request, 'sell_login.html', {'error': error})




def sell_logout(request):
    request.session.clear()
    return redirect('start')




# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth import update_session_auth_hash
# from django.shortcuts import render, redirect
# from django.contrib import messages

# @login_required
# def sell_change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             # update the session to prevent logging out the user
#             update_session_auth_hash(request, user)
#             messages.success(request, 'Your password has been changed successfully!')
#             return redirect('homepage')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'sell_change_password.html', {'form': form})


# @login_required(login_url='sell_login/')
# def sell_edit_account(request):
#     user = request.user
#     seller = user.seller

#     if request.method == 'POST':
#         # Update seller information
#         seller.first_name = request.POST.get('first_name')
#         seller.last_name = request.POST.get('last_name')
#         seller.phone = request.POST.get('phone')
#         seller.location = request.POST.get('location')

#         # Update seller images
#         if request.FILES.get('store_image'):
#             seller.store_image = request.FILES.get('store_image')
#         if request.FILES.get('qr_image'):
#             seller.qr_image = request.FILES.get('qr_image')

#         try:
#             seller.save() # save the updated seller information to the database
#             messages.success(request, 'Account updated successfully.')
#         except Exception as e:
#             messages.error(request, 'Failed to update account: {}'.format(e))

#     return render(request, 'sell_edit_account.html', {'seller': request.user.seller})


@login_required(login_url='/sell_login/')
def sell_edit_account(request):
    # Get seller by email
    
    email = request.user.username
    seller = Seller.objects.get(email=email)

    if request.method == 'POST':
        # Get form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        store_name = request.POST['store_name']
        phone = request.POST['phone']
        location = request.POST['location']
      
        

        # Validate input
        error_message = None
        if len(first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif len(last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif len(phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif not re.match(r'^(\+66|0)\d{9}$',phone):
            error_message ="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'"
        elif Seller.objects.filter(email=email).exclude(id=seller.id).exists():
            error_message = 'Email Address Already Registered..'
        else:
            # Update user
            user = seller.created_by
            if user.is_authenticated:
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            # Update seller
            seller.first_name = first_name
            seller.last_name = last_name
            seller.store_name = store_name
            seller.phone = phone
            seller.location = location

            # Get password confirmation
            if request.FILES.get('store_image'):
                seller.store_image = request.FILES.get('store_image')
            if request.FILES.get('qr_image'):
                seller.qr_image = request.FILES.get('qr_image')
            
           
            seller.save()
            try:
                seller.save() # save the updated seller information to the database
                messages.success(request, 'Account updated successfully.')
            except Exception as e:
                messages.error(request, 'Failed to update account: {}'.format(e))
            return redirect('sell_edit_account')

    return render(request, 'sell_edit_account.html', {'seller': request.user.seller})



@login_required
def seller_admin(request):
    # products = Products.objects.filter(seller=request.user.seller)
    # return render(request, 'seller_admin.html', {'products': products})
    seller = request.user.seller
    products = seller.products.all()
    return render(request, 'seller_admin.html', {'seller': seller, 'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False) # Because we have not given vendor yet
            product.seller = request.user.seller
            product.slug = slugify(product.name)
            product.save() #finally save

            return redirect('seller_admin')

    else:
        form = ProductForm

    return render(request, 'add_product.html', {'form': form})



# def sell_edit_product(request, product_id):
#     product = get_object_or_404(Products, pk=product_id)
#     if request.method == 'POST':
#         # Update the product object with the data submitted in the form
#         product.name = request.POST['name']
#         product.price = request.POST['price']
#         product.category = request.POST['category']
#         product.stockqty = request.POST['stockqty']
#         product.save()
#         # Redirect to the seller admin page
#         return redirect('seller_admin')
#     else:
#         # Render the edit product form with the product object
#         return render(request, 'sell_edit_product.html', {'product': product})


# from django.shortcuts import get_object_or_404, redirect, render
# from .models import Category, Products

# def sell_edit_product(request, product_id):
#     # Retrieve the product instance with the given ID
#     product = get_object_or_404(Products, pk=product_id)
#     if request.method == 'POST':
#         # Retrieve the category instance with the given name from the database
#         category_name = request.POST['category']
#         category = get_object_or_404(Category, name=category_name)
#         # Update the product object with the data submitted in the form
#         product.name = request.POST['name']
#         product.price = request.POST['price']
#         product.category = category
#         product.stockqty = request.POST['stockqty']
#         product.save()
#         # Redirect to the seller admin page
#         return redirect('seller_admin')
#     else:
#         # Render the edit product form with the product object
#         return render(request, 'sell_edit_product.html', {'product': product})

from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Products

def sell_edit_product(request, product_id):
    # Retrieve the product instance with the given ID
    product = get_object_or_404(Products, pk=product_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        # Retrieve the category instance with the given name from the database
        category_name = request.POST['category']
        category = get_object_or_404(Category, name=category_name)
        # Update the product object with the data submitted in the form
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.category = category
        product.stockqty = request.POST['stockqty']
        product.save()
        # Redirect to the seller admin page
        return redirect('seller_admin')
    else:
        # Render the edit product form with the product object and categories
        return render(request, 'sell_edit_product.html', {'product': product, 'categories': categories})


# def sell_delete_product(request, product_id):
#     # Retrieve the product instance with the given ID
#     product = get_object_or_404(Products, pk=product_id)
#     # Delete the product from the database
#     product.delete()
#     # Redirect back to the seller admin page
#     return redirect('seller_admin')

from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Products

def sell_delete_product(request, product_id):
    # Retrieve the product instance with the given ID
    product = get_object_or_404(Products, pk=product_id)
    if request.method == 'POST':
        # Delete the product object from the database
        product.delete()
        # Redirect to the seller admin page
        return redirect('seller_admin')
    else:
        # Render the delete product confirmation page
        return render(request, 'sell_delete_product.html', {'product': product})


