import logging

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import BaseDocument
from .forms import DocumentForm

@login_required
def home(request):
    base_document = BaseDocument.objects.all()
    return render(request, 'norm_proc_app/home.html', {'base_document': base_document})

@login_required
def create_procedure(request):
    return HttpResponse("Create procedure page - to be implemented")

@login_required
def create_document(request):
    logging.basicConfig(level=logging.INFO)
    if request.method == 'POST':
        # Lógica para processar o formulário de criação de norma
        print(request.FILES)
        
        norm_form = DocumentForm(request.POST, request.FILES)
        if norm_form.is_valid():
            # Salvar a nova norma
            new_norm = norm_form.save(commit=False)
            new_norm.author = request.user
            new_norm.save()
            messages.success(request, "Document created successfully!")
            return HttpResponseRedirect(reverse(
                'norm_proc_app:document_details',
                kwargs={'document_id': new_norm.pk}
            ))

        logging.error(f"Norm form errors: {norm_form.errors}")
        messages.error(request, "There was an error creating the norm.")
        return render(request, 'norm_proc_app/create_norm.html', {'form': norm_form})

    norm_form = DocumentForm()
    return render(request, 'norm_proc_app/create_norm.html', {'form': norm_form})

@login_required
def update_document(request, document_id):
    # TODO: Rever em como implementar a função `create_new_version` do modelo `BaseDocument`.
    document = get_object_or_404(BaseDocument, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Document updated successfully!")
            return HttpResponseRedirect(reverse(
                'norm_proc_app:document_details',
                kwargs={'document_id': document.pk}
            ))
        else:
            messages.error(request, "There was an error updating the document.")
    else:
        form = DocumentForm(instance=document)

    return render(request, 'norm_proc_app/update_document.html', {'form': form, 'document': document})

@login_required
def document_list(request):
    documents = BaseDocument.objects.order_by("document_type", "title")
    documents_by_type = {}
    for document in documents:
        document_type = document.get_document_type_display()
        documents_by_type.setdefault(document_type, []).append(document)

    return render(request, 'norm_proc_app/document_list.html', {
        'documents': documents,
        'documents_by_type': documents_by_type,
    })

@login_required
def document_details(request, document_id):
    document = get_object_or_404(BaseDocument, id=document_id)
    return render(request, 'norm_proc_app/document_details.html', {"document": document});

@login_required
@require_POST
def submit_document_for_review(request, document_id):
    document = get_object_or_404(BaseDocument, id=document_id)

    if document.status != "draft":
        return JsonResponse(
            {"error": "O documento já não está em estado de rascunho."},
            status=400,
        )

    document.status = "under_review"
    document.save(update_fields=["status"])
    return JsonResponse({"status": document.status})

@login_required
@require_POST
def submit_document_for_approval(request, document_id):
    document = get_object_or_404(BaseDocument, id=document_id)

    if document.status != "under_review":
        return JsonResponse(
            {"error": "O documento não está em estado de revisão."},
            status=400,
        )

    document.status = "pending_approval"
    document.save(update_fields=["status"])
    return JsonResponse({"status": document.status})


@login_required
@require_POST
def approve_document(request, document_id):
    document = get_object_or_404(BaseDocument, id=document_id)

    if document.status != "pending_approval":
        return JsonResponse(
            {"error": "O documento não está em estado de aprovação."},
            status=400,
        )

    document.status = "approved"
    document.save(update_fields=["status"])
    return JsonResponse({"status": document.status})

@login_required
def procedure_details(request, procedure_id):
    return HttpResponse(f"Procedure details page for procedure_id: {procedure_id} - to be implemented")

@login_required
def viewer(request, id):
    document = BaseDocument.objects.get(id=id)
    return render(request, "norm_proc_app/viewer.html", {"document": document})
