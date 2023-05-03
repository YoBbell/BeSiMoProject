from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Category, Products, Customer, Order
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .forms import SignupForm
from .models import Customer, Order

class Cart:
    def get(self, request):
        ids = list(request.session.get('cart', {}).keys())
        products = Products.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html', {'products': products})

class CheckOut:
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart', {})
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


class Index:
    def post(self, request):
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

    def get(self, request):
        return HttpResponseRedirect('/store' + request.get_full_path()[1:])

def store(request):
    cart = request.session.get('cart', {})
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()

    data = {
        'products': products,
        'categories': categories
    }

    print('you are: ', request.session.get('email'))
    return render(request, 'index.html', data)


class Login:
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Invalid credentials'
        else:
            error_message = 'Invalid credentials'

        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')



class OrderView:
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})

<<<<<<< Updated upstream

# def product_detail(request, slug, id):
#     product = Product.objects.get(id=id)
#     return render(request, 'product_detail.html', {'data': product})

# def product_browse(request):
#     products = Product.objects.all()
#     print(f"products items: {products}")
#     return render(request, 'product_browse.html' ,{'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def product_browse(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(collection=category).order_by('-last_update')
    return render(request, 'product_browse.html', {'category': category, 'products': products})
=======
class Signup:
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        else:
            return HttpResponse(form.errors.as_json(), status=400)
>>>>>>> Stashed changes
