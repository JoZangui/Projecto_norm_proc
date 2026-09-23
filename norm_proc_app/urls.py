# norm_proc_app/urls.py
from django.urls import path
from . import views

app_name = 'norm_proc_app'

urlpatterns = [
    # home
    path('', views.home, name='home'),

    # --------- Norms urls -------
    # create norm
    path('create_norm/', views.create_norm, name='create_norm'),
    # norm details page
    path('norm_details/<uuid:norm_id>/', views.norm_details, name='norm_details'),
    # submit for review
    path('norm_details/<uuid:norm_id>/submit-for-review/', views.submit_norm_for_review, name='submit_norm_for_review'),
    # submit for approval
    path('norm_details/<uuid:norm_id>/submit-norm-for-approval/', views.submit_norm_for_approval, name='submit_norm_for_approval'),
    # approve
    path('norm_details/<uuid:norm_id>/approve-norm/', views.approve_norm, name='approve_norm'),

    # --------- Procedures urls -------

    # procedure details page
    path('procedure_details/<uuid:procedure_id>/', views.procedure_details, name='procedure_details'),
    # create new procedure
    path('create_procedure/', views.create_procedure, name='create_procedure'),
    # path("viewer/", views.viewer, name="viewer"),
    path("viewer/<uuid:id>/", views.viewer, name="viewer")
]