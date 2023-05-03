# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import AuthenticationForm
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login
# from .forms import BuyerForm
# from .models import Category, Product

# # def signup(request):
# #     if request.method == 'POST':
# #         form = BuyerForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             login(request, user)
# #             return redirect('success')
# #     else:
# #         form = BuyerForm()
# #     return render(request, 'signup.html', {'form': form})

# # def signup(request):
# #     if request.method == 'POST':
# #         form = BuyerForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             login(request, user)
# #             return redirect('success')
# #         else:
# #             if form.cleaned_data.get('password') != form.cleaned_data.get('password_again'):
# #                 form.add_error('password_again', 'Passwords do not match')
# #     else:
# #         form = BuyerForm()
# #     return render(request, 'signup.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = BuyerForm(request.POST)
#         if form.is_valid():
#             if form.cleaned_data.get('password') != form.cleaned_data.get('password_again'):
#                 form.add_error('password_again', 'Passwords do not match')
#             else:
#                 user = form.save()
#                 login(request, user)
#                 return redirect('success')
#     else:
#         form = BuyerForm()
#     return render(request, 'signup.html', {'form': form})

# def register(request):
#     return render(request, "register.html")


# def success(request):
#     return render(request, 'success.html')


# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 form.add_error(None, 'Invalid username or password')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})



# def category_browse(request):
#     categories = Category.objects.all()
#     print(f"category items: {categories}")
#     return render(request, 'category_browse.html' ,{'categories': categories})


# def product_detail(request, slug, id):
#     product = Product.objects.get(id=id)
#     return render(request, 'product_detail.html', {'data': product})
# # def product_browse(request):
# #     products = Product.objects.all()
# #     print(f"products items: {products}")
# #     return render(request, 'product_browse.html' ,{'products': products})

# def product_browse(request, category_id):
#     category = get_object_or_404(Category, pk=category_id)
#     products = Product.objects.filter(collection=category).order_by('-last_update')
#     return render(request, 'product_browse.html', {'category': category, 'products': products})


from django.shortcuts import render , redirect

from django.contrib.auth.hashers import  check_password
from .models import Customer
from django.views import  View
from .models import Products

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products} )

from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from .models import Customer
from django.views import View

from .models import Products
from .models import Order


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')

from django.shortcuts import render , redirect , HttpResponseRedirect
from .models import Products
from .models import Category
from django.views import View


# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/accounts{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from .models import Customer
from django.views import View


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print (email, password)
        return render (request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

    from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Customer
from django.views import View
from .models import Products
from .models import Order
from .middlewares.auth import auth_middleware

class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})



from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Customer
from django.views import View


class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer (customer)

        if not error_message:
            print (first_name, last_name, phone, email, password)
            customer.password = make_password (customer.password)
            customer.register ()
            return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message

