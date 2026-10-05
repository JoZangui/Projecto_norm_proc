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
def create_document(request):
    logging.basicConfig(level=logging.INFO)
    if request.method == 'POST':
        # Lógica para processar o formulário de criação de norma
        print(request.FILES)

        document_form = DocumentForm(request.POST, request.FILES)
        if document_form.is_valid():
            # Salvar a nova norma
            new_norm = document_form.save(commit=False)
            new_norm.author = request.user
            new_norm.save()
            messages.success(request, "Document created successfully!")
            return HttpResponseRedirect(reverse(
                'norm_proc_app:document_details',
                kwargs={'document_id': new_norm.pk}
            ))

        logging.error(f"Norm form errors: {document_form.errors}")
        messages.error(request, "There was an error creating the norm.")
        return render(request, 'norm_proc_app/create_document.html', {'form': document_form})

    document_form = DocumentForm()
    return render(request, 'norm_proc_app/create_document.html', {'form': document_form})

@login_required
def create_document_new_version(request):
    # TODO: Implementar a lógica para criar uma nova versão de um documento
    # TODO: Rever em como implementar a função `create_new_version` do modelo `BaseDocument`.
    logging.info("Creating a new version of a document - to be implemented")
    if request.method == 'POST':
        document_form = DocumentForm(request.POST, request.FILES)
        if document_form.is_valid():
            # Salvar a nova versão do documento
            new_version = document_form.save(commit=False)
            major_v, minor_v = map(int, new_version.current_version.split("."))

            # TODO: Por trabalhar em como determinar se é uma nova versão maior ou menor, talvez com um campo no formulário.
            if 'major' in request.POST:
                major_v += 1
                minor_v = 0
            else:
                minor_v += 1
            new_version.current_version = f"{major_v}.{minor_v}"

            new_version.author = request.user
            new_version.save()
            messages.success(request, "New version of the document created successfully!")
            return HttpResponseRedirect(reverse(
                'norm_proc_app:document_details',
                kwargs={'document_id': new_version.pk}
            ))
        logging.error(f"Document form errors: {document_form.errors}")
        messages.error(request, "There was an error creating the new version of the document.")
    document_form = DocumentForm()
    return render(request, 'norm_proc_app/create_document_new_version.html', {'form': document_form})


@login_required
def update_document(request, document_id):
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
def viewer(request, id):
    document = BaseDocument.objects.get(id=id)
    return render(request, "norm_proc_app/viewer.html", {"document": document})
