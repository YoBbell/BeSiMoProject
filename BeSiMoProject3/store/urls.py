from django.contrib import admin
from .middlewares.auth import  auth_middleware
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='homepage'),
    path('store/', views.index , name='store'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('cart/login/', views.login, name='login'),
    path('logout/', views.logout , name='logout'),
    path('cart/', auth_middleware(views.cart) , name='cart'),
    path('check-out/', views.checkout , name='checkout'),
    path('orders/', auth_middleware(views.orders), name='orders'),

]
