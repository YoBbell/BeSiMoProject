from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('sell_signup/', views.sell_signup, name='sell_signup'),
    path('sell_login/', views.sell_login, name='sell_login'),
    path('sell_account/', views.sell_account, name='sell_account'),
    path('logout/', views.logout, name='logout'),
    # path('sell_product/', views.sell_product, name='sell_product'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

