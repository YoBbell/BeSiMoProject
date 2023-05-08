from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('sell_signup/', views.sell_signup, name='sell_signup'),
    path('sell_login/', views.sell_login, name='sell_login'),
    path('sell_edit_account/', views.sell_edit_account, name='sell_edit_account'),
    # path('sell_change_password/', views.sell_change_password, name='sell_change_password'),
    path('sell_logout/', views.sell_logout, name='sell_logout'),
    path('seller_admin/', views.seller_admin, name="seller_admin"),
    path('seller_admin/add_product/', views.add_product, name="add_product"),
    path('seller_admin/sell_edit_product/<int:product_id>', views.sell_edit_product, name="sell_edit_product"),
    path('seller_admin/products/category/<int:category_id>/', views.sell_product_by_category, name='sell_product_by_category'),
    path('seller_admin/products/category/<int:category_id>/add_product/', views.add_product_by_category, name='add_product_by_category'),
    path('sell_delete_product/<int:product_id>', views.sell_delete_product, name='sell_delete_product'),
    path('seller_payment/', views.seller_payment, name='seller_payment'),
    path('seller_payment/<int:order_id>', views.update_order_status, name='update_order_status')

    # path('sell_product/', views.sell_product, name='sell_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

