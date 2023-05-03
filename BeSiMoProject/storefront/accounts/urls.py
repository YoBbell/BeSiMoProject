from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('success/', views.success, name='success'),
    path('login/', views.login_view, name='login'),
    path('category_browse/', views.category_browse, name='category_browse'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category_browse/<int:category_id>/', views.product_browse, name='product_browse')
    # path('product_browse/', views.product_browse, name='product_browse')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
