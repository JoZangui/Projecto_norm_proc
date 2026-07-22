from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .forms import NormForm

@login_required
def home(request):
    return render(request, 'norm_proc_app/home.html')

@login_required
def create_new_request(request):
    return render(request, 'norm_proc_app/create_new_request.html')

@login_required
def create_procedure(request):
    return HttpResponse("Create procedure page - to be implemented")

@login_required
def create_norm(request):
    if request.method == 'POST':
        # Lógica para processar o formulário de criação de norma
        norm_form = NormForm(request.POST)
        if norm_form.is_valid():
            # Salvar a nova norma
            norm_form.save()
            messages.success(request, "Norm created successfully!")
            # return HttpResponse("Norm created successfully!")
            return HttpResponseRedirect(reverse(
                'norm_proc_app:home',
                kwargs={'norm_id': norm_form.instance.pk}
            ))

        messages.error(request, "There was an error creating the norm.")
        return render(request, 'norm_proc_app/create_norm.html', {'form': norm_form})

    norm_form = NormForm()
    return render(request, 'norm_proc_app/create_norm.html', {'form': norm_form})

@login_required
def norm_details(request, norm_id):
    return HttpResponse(f"Norm details page for norm_id: {norm_id} - to be implemented")

@login_required
def procedure_details(request, procedure_id):
    return HttpResponse(f"Procedure details page for procedure_id: {procedure_id} - to be implemented")
