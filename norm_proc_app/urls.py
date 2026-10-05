# norm_proc_app/urls.py
from django.urls import path
from . import views

app_name = 'norm_proc_app'

urlpatterns = [
    # home
    path('', views.home, name='home'),
    # create document
    path('create_document/', views.create_document, name='create_document'),
    # document details page
    path('document_details/<uuid:document_id>/', views.document_details, name='document_details')
]