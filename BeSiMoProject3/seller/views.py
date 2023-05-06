from django.shortcuts import render, redirect, HttpResponseRedirect
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
            return redirect('sell_edit_account') # เดี๋ยวมาเชื่อมอีกที
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





def seller_admin(request):
    queryset = Products.objects.all()
    items = []
    for item in queryset:
        items.append(item)
    return render(request, "seller_admin.html", {'items': items})
