from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



# urlpatterns = [
#     path('signup/', views.signup, name='signup'),
#     path('success/', views.success, name='success'),
#     path('login/', views.login_view, name='login')
# ]

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('success/', views.success, name='success'),
    path('login/', views.login_view, name='login'),
    path('category_browse/', views.category_browse, name='category_browse')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
