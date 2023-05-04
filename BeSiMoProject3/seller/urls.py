from django.urls import path
from . import views

urlpatterns = [
    path('sell_signup/', views.sell_signup , name='sell_signup'),
    path('sell_login/', views.sell_login, name='sell_login'),
    path('sell_account/', views.seller_account, name='sell_account')

]
