from django.contrib import admin
from .middlewares.auth import  auth_middleware
from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='homepage'),
    path('start/', views.start, name='start'),
    path('store/', views.index , name='store'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('cart/login', views.login_user, name='cart_login'),
    path('login/store/', views.index, name='login_store'),
    path('logout/', views.logout , name='logout'),
    path('cart/', auth_middleware(views.cart) , name='cart'),
    path('check-out/', views.checkout , name='checkout'),
    path('orders/', auth_middleware(views.orders), name='orders'),
    path('product/<int:id>', views.product_detail, name="product_detail"),
    path('brand_list/', views.brand_list, name="brand_list"),
    path('brand_product_list/<int:store_id>', views.brand_product_list, name="brand_product_list"),
    path('edit_account/', views.edit_account, name='edit_account'),
]
