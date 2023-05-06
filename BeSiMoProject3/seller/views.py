from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password,  check_password
from .models import *
from django.views import View
import re
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Seller, Item


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


@login_required(login_url='sell_login/')
def sell_edit_account(request):
    user = request.user
    seller = user.seller

    if request.method == 'POST':
        # Update seller information
        seller.first_name = request.POST.get('first_name')
        seller.last_name = request.POST.get('last_name')
        seller.phone = request.POST.get('phone')
        seller.location = request.POST.get('location')

        # Update seller images
        if request.FILES.get('store_image'):
            seller.store_image = request.FILES.get('store_image')
        if request.FILES.get('qr_image'):
            seller.qr_image = request.FILES.get('qr_image')

        try:
            seller.save() # save the updated seller information to the database
            messages.success(request, 'Account updated successfully.')
        except Exception as e:
            messages.error(request, 'Failed to update account: {}'.format(e))

    return render(request, 'sell_edit_account.html', {'seller': request.user.seller})


# @login_required
def seller_admin(request):
    # vendor = request.seller
    # products = vendor.products.all()
    # orders = vendor.orders.all()
    # for order in orders:
    #     order.vendor_amount = 0
    #     order.vendor_paid_amount = 0
    #     order.fully_paid = True

    #     for item in order.items.all():
    #         if item.vendor == request.user.vendor:
    #             if item.vendor_paid:
    #                 order.vendor_paid_amount += item.get_total_price()
    #             else:
    #                 order.vendor_amount += item.get_total_price()
    #                 order.fully_paid = False
    # return render(request, 'vendor_admin.html', {'vendor': vendor})

# #--------------------------------------------
# # queryset = Product.objects.all()
    # queryset = Item.objects.all()
    # for Item in queryset:
    #     print(Item)
    # return render(request, "vendor_admin.html", {'Item': Item})

# def logout(request):
    # request.session.clear()
    # return redirect('vender_admin.html')
    # return render(request, 'vendor_admin.html', {'vendor': vendor})


    queryset = Item.objects.all()
    items = []
    for item in queryset:
        items.append(item)
    return render(request, "seller_admin.html", {'items': items})
