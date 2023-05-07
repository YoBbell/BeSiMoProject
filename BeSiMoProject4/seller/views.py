from http.client import HTTPResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password,  check_password
from .models import *
from django.views import View
import re
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm
from django.utils.text import slugify



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
        store_name = request.POST.get('store_name')

        error_message = None
        # validation
        if not store_name:
            error_message = "Please Enter your Store Name !!"
        elif len(store_name) < 1:
            error_message = "Please Enter your Store Name !!"
        elif not first_name:
            error_message = "Please Enter your First Name !!"
        elif len(first_name) < 3:
            error_message = 'First Name must be 3 characters long or more'
        elif not last_name:
            error_message = 'Please Enter your Last Name'
        elif len(last_name) < 3:
            error_message = 'Last Name must be 3 characters long or more'
        elif not phone:
            error_message = 'Enter your Phone Number !!'
        elif len(phone) < 10:
            error_message = 'Phone Number must be 10 characters Long'
        elif len(password) < 5:
            error_message = 'Password must be 5 characters long'
        elif len(email) < 5:
            error_message = 'Email must be 5 characters long'
        elif not re.match(r'^\d{9,11}\@student\.chula\.ac\.th$', email):
            error_message = 'Email must be in the format: 6xxxxxxxxx@student.chula.ac.th'
        elif Seller.objects.filter(email=email).exists():
            error_message = 'Email Address Already Registered..'
        else:
            seller = Seller(first_name=first_name,
                                last_name=last_name,
                                store_name=store_name,
                                phone=phone,
                                email=email,
                                password=make_password(password),
                                location=location,
                                store_image=store_image,
                                qr_image=qr_image)
            seller.save()
            return redirect('sell_product')

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

# ----------------------------------------------------------------
def vendors(request):
    return render(request, 'vendors.html')
# ----------------------------------------------------------------
@login_required
def vendor_admin(request):
    # vendor = request.user.vendor
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()
    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False
    return render(request, 'vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders})

#-------------------------------------------------------------------
# @login_required(login_url='/auth/login')
# def view_item(request, shop_id, item_id):
#     shop = Seller.objects.get(shop_id=shop_id)
#     item = Item.objects.get(item_id=item_id)
#     images = ItemPicture.objects.filter(item_id=item_id)

#     return render(request, "seller/view-item.html", {
#         "shop": shop,
#         "item": item,
#         "image0": images[0],
#         "images": images[1:]
#     })
#-------------------------------------------------------------------
# @login_required
# def view_shop(request, created_by):
#     shop = Seller.objects.get(created_by=created_by)
#     if shop.user_id != request.user.id:
#         return HTTPResponse("403")

#     items = Item.objects.filter(created_by=created_by)
#     data = []

#     for item in items:
#         order = OrderItem.objects.filter(item_id=item.item_id, order_status=0)
#         if len(order) != 0:
#             data.append([o for o in order])

#     items_data = []
#     for item in items:
#         img = ItemPicture.objects.filter(item_id=item.item_id)[0]
#         items_data.append([item, img])

#     return render(request, "shop.html", {
#         "data": data,
#         "data_length": len(data),
#         "items": items_data
#     })
#-------------------------------------------------------------------
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False) # Because we have not given vendor yet
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save() #finally save

            return redirect('vendor-admin')

    else:
        form = ProductForm

    return render(request, 'add_product.html', {'form': form})