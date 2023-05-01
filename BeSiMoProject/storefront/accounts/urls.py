from django.urls import path
from . import views

# urlpatterns = [
#     path('signup/', views.signup, name='signup'),
#     path('success/', views.success, name='success'),
#     path('login/', views.login_view, name='login')
# ]

urlpatterns = [
    path("register", views.register, name="register"),
]