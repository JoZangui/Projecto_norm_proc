# norm_proc_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_norm/', views.create_norm, name='create_norm'),
    path('create_procedure/', views.create_procedure, name='create_procedure'),
    path('create_new_request/', views.create_new_request, name='create_new_request'),
    path('norm_details/<int:norm_id>/', views.norm_details, name='norm_details'),
    path('procedure_details/<int:procedure_id>/', views.procedure_details, name='procedure_details'),
]