from django.urls import path
from . import views

urlpatterns = [
    path('seller_signup/', views.seller_signup, name='seller_signup'),
    path('seller_signup_success/', views.seller_signup_success, name='seller_signup_success'),
    path('seller_change/', views.seller_change, name='seller_change'),
]
