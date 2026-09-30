# norm_proc_app/urls.py
from django.urls import path
from . import views

app_name = 'norm_proc_app'

urlpatterns = [
    # home
    path('', views.home, name='home'),

    # --------- Norms urls -------
    # create document
    path('create_document/', views.create_document, name='create_document'),
    # document details page
    path('document_details/<uuid:document_id>/', views.document_details, name='document_details'),
    # submit for review
    path('document_details/<uuid:document_id>/submit-for-review/', views.submit_document_for_review, name='submit_document_for_review'),
    # submit for approval
    path('document_details/<uuid:document_id>/submit-document-for-approval/', views.submit_document_for_approval, name='submit_document_for_approval'),
    # approve
    path('document_details/<uuid:document_id>/approve-document/', views.approve_document, name='approve_document'),

    # --------- Procedures urls -------

    # procedure details page
    path('procedure_details/<uuid:procedure_id>/', views.procedure_details, name='procedure_details'),
    # create new procedure
    path('create_procedure/', views.create_procedure, name='create_procedure'),
    # path("viewer/", views.viewer, name="viewer"),
    path("viewer/<uuid:id>/", views.viewer, name="viewer")
]