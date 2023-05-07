from django.urls import path
from . import views


urlpatterns = [
    path('sell_signup/', views.sell_signup, name='sell_signup'),
    path('sell_login/', views.sell_login, name='sell_login'),
    path('sell_account/', views.sell_account, name='sell_account'),
    path('logout/', views.logout, name='logout'),
    path('vendor-admin/', views.vendor_admin, name="vendor-admin"),
    path('add-product/', views.add_product, name="add-product"),
    # path('view_shop/', views.view_shop, name="view_shop"),
    # path("shop/<uuid:shop_id>/items/<uuid:item_id>/", views.view_item)


    # path('sell_product/', views.sell_product, name='sell_product'),
]

