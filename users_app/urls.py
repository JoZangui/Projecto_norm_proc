""" users_app/urls.py """
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # path('login/', views.LoginView.as_view(), name='login'),
    path("login/", views.user_login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='norm_proc_app/home.html'), name='logout'),
    path('register_success/', views.register_success, name='register_success')
]
