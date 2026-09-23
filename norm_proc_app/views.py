import logging

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Norms
from .forms import NormForm

@login_required
def home(request):
    return render(request, 'norm_proc_app/home.html')

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
    norm = get_object_or_404(Norms, id=norm_id)
    return render(request, 'norm_proc_app/norm_details.html', {"norm": norm});

@login_required
@require_POST
def submit_norm_for_review(request, norm_id):
    norm = get_object_or_404(Norms, id=norm_id)

    if norm.status != "draft":
        return JsonResponse(
            {"error": "A norma já não está em estado de rascunho."},
            status=400,
        )

    norm.status = "under_review"
    norm.save(update_fields=["status"])
    return JsonResponse({"status": norm.status})

@login_required
@require_POST
def submit_norm_for_approval(request, norm_id):
    norm = get_object_or_404(Norms, id=norm_id)

    if norm.status != "under_review":
        return JsonResponse(
            {"error": "A norma não está em estado de revisão."},
            status=400,
        )

    norm.status = "pending_approval"
    norm.save(update_fields=["status"])
    return JsonResponse({"status": norm.status})


@login_required
@require_POST
def approve_norm(request, norm_id):
    norm = get_object_or_404(Norms, id=norm_id)

    if norm.status != "pending_approval":
        return JsonResponse(
            {"error": "A norma não está em estado de aprovação."},
            status=400,
        )

    norm.status = "approved"
    norm.save(update_fields=["status"])
    return JsonResponse({"status": norm.status})

@login_required
def procedure_details(request, procedure_id):
    return HttpResponse(f"Procedure details page for procedure_id: {procedure_id} - to be implemented")

@login_required
def viewer(request, id):
    norm = Norms.objects.get(id=id)
    return render(request, "norm_proc_app/viewer.html", {"norm": norm})
