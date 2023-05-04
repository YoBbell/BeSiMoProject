from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password,  check_password
from .models import *
from django.views import View
import re
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def sell_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get("location")
        store_image = request.POST.get('store_image')
        qr_image = request.POST.get('qr_image')

        # validation
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
        elif Seller.objects.filter(email=email).exists():
            error_message = 'Email Address Already Registered..'
        else:
            seller = Seller(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                password=password,
                                location=location,
                                store_image=store_image,
                                qr_image=qr_image)
            seller.save()
            return redirect('sell_login')

        data = {
            'error': error_message,
            'values': request.POST
        }
        return render(request, 'sell_signup.html', data)

    return render(request, 'sell_signup.html')

def sell_login(request):
    return_url = None
    if request.method == 'GET':
        return_url = request.GET.get('return_url')
        return render(request, 'sell_login.html')

    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        seller = Seller.objects.filter(email=email).first()
        error_message = None

        if seller:
            flag = check_password(password, seller.password)
            if flag:
                request.session['seller'] = seller.id

                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return redirect('homepage')
            else:
                error_message = 'Invalid password'
        else:
            error_message = 'Seller not found'

        return render(request, 'sell_login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('sell_login')


@login_required
def seller_account(request):
    try:
        seller = Seller.objects.get(email=request.user.email)
    except Seller.DoesNotExist:
        seller = None

    if request.method == 'POST' and seller:
        # Update seller object with new data from form
        seller.first_name = request.POST.get('first_name', seller.first_name)
        seller.last_name = request.POST.get('last_name', seller.last_name)
        seller.phone = request.POST.get('phone', seller.phone)
        seller.location = request.POST.get('location', seller.location)

        # Check if a new profile image was uploaded
        if request.FILES.get('store_image'):
            seller.store_image = request.FILES['store_image']

        # Check if a new QR code image was uploaded
        if request.FILES.get('qr_image'):
            seller.qr_image = request.FILES['qr_image']

        # Save updated seller object
        seller.save()

        messages.success(request, 'Your account information has been updated.')

        return redirect('sell_account')

    context = {
        'seller': seller
    }

    return render(request, 'sell_account.html', context)

# @login_required
# def seller_account(request):
#     if request.method == 'POST':
#         # Get seller object based on user's email
#         seller = Seller.objects.get(email=request.user.email)
        
#         # Update seller object with new data from form
#         seller.first_name = request.POST['first_name']
#         seller.last_name = request.POST['last_name']
#         seller.phone = request.POST['phone']
#         seller.location = request.POST['location']
        
#         # Check if a new profile image was uploaded
#         if request.FILES.get('store_image'):
#             seller.store_image = request.FILES['store_image']
        
#         # Check if a new QR code image was uploaded
#         if request.FILES.get('qr_image'):
#             seller.qr_image = request.FILES['qr_image']
        
#         # Save updated seller object
#         seller.save()
        
#         messages.success(request, 'Your account information has been updated.')
        
#         return redirect('sell_account')
        
#     else:
#         # Get seller object based on user's email
#         seller = Seller.objects.get(email=request.user.email)
        
#         context = {
#             'seller': seller
#         }
        
#         return render(request, 'sell_account.html', context)
