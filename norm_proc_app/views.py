import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Norms
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
    logging.basicConfig(level=logging.INFO)
    if request.method == 'POST':
        # Lógica para processar o formulário de criação de norma
        print(request.FILES)
        
        norm_form = NormForm(request.POST, request.FILES)
        if norm_form.is_valid():
            # Salvar a nova norma
            new_norm = norm_form.save(commit=False)
            new_norm.author = request.user
            new_norm.save()
            messages.success(request, "Norm created successfully!")
            return HttpResponseRedirect(reverse(
                'norm_proc_app:norm_details',
                kwargs={'norm_id': new_norm.pk}
            ))

        logging.error(f"Norm form errors: {norm_form.errors}")
        messages.error(request, "There was an error creating the norm.")
        return render(request, 'norm_proc_app/create_norm.html', {'form': norm_form})

    norm_form = NormForm()
    return render(request, 'norm_proc_app/create_norm.html', {'form': norm_form})

@login_required
def norm_details(request, norm_id):
    # return HttpResponse(f"Norm details page for norm_id: {norm_id} - to be implemented")

    norm = Norms.objects.get(id=norm_id)
    return render(request, 'norm_proc_app/norm_details.html', {"norm": norm});

@login_required
def procedure_details(request, procedure_id):
    return HttpResponse(f"Procedure details page for procedure_id: {procedure_id} - to be implemented")
