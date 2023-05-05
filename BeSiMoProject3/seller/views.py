from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password,  check_password
from .models import *
from django.views import View
import re
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings



from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Seller

def sell_signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        store_name = request.POST['store_name']
        password = request.POST['password']
        phone = request.POST['phone']
        email = request.POST['email']
        location = request.POST['location']
        store_image = request.FILES['store_image']
        qr_image = request.FILES['qr_image']

        # create a new user
        user = User.objects.create_user(username=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # create a new seller
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
            created_by=user
        )
        seller.save()

        messages.success(request, 'Your account has been created successfully!')
        return redirect('sell_login')

    return render(request, 'sell_signup.html')





def sell_login(request):
    return_url = None
    if request.method == 'GET':
        return_url = request.GET.get('return_url')
        return render(request, 'sell_login.html')

    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        seller = Seller.get_seller_by_email(email)
        error_message = None

        if seller:
            flag = check_password(password, seller.password)
            if flag:
                request.session['seller'] = seller.id

                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return redirect('sell_product')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print(email, password)
        return render(request, 'sell_login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('sell_login')

@login_required
def sell_account(request):
    try:
        seller = Seller.objects.get(email=request.user.email)
    except Seller.DoesNotExist:
        seller = None

    if request.method == 'POST' and seller:
        # Update seller object with new data from form
        seller.first_name = request.POST.get('first_name', seller.first_name)
        seller.last_name = request.POST.get('last_name', seller.last_name)
        seller.store_name = request.POST.get('store_name', seller.store_name)
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
