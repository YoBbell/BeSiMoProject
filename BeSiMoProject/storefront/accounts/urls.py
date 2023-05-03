from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



# # urlpatterns = [
# #     path('signup/', views.signup, name='signup'),
# #     path('success/', views.success, name='success'),
# #     path('login/', views.login_view, name='login')
# # ]

# urlpatterns = [
#     path('signup/', views.signup, name='signup'),
#     path('success/', views.success, name='success'),
#     path('login/', views.login_view, name='login'),
#     path('category_browse/', views.category_browse, name='category_browse'),
#     path('product/<int:product_id>/', views.product_detail, name='product_detail')
#     path('category_browse/<int:category_id>/', views.product_browse, name='product_browse')
#     # path('product_browse/', views.product_browse, name='product_browse')
# ]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from .views import Index , store
from .views import Signup
from .views import Login , logout
from .views import Cart
from .views import CheckOut
from .views import OrderView
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),

    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

]
