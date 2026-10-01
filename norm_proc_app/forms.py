from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import BaseDocument

User = get_user_model()

class DocumentForm(ModelForm):
    class Meta:
        model = BaseDocument
        fields = [
            'title',
            'file',
            'Description',
            'document_type',
            'Classification_level',
            'reviewed_by', # Adicionado para permitir a seleção do revisor do documento
            'approved_by', # Adicionado para permitir a seleção do aprovador do documento
            'document_owner', # Adicionado para permitir a seleção do departamento proprietário do documento
            'Recipient' # Adicionado para permitir a seleção do destinatário do documento (Se for para todos só precisamos selecionar a opção "Todos")
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'documentFile'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'Recipient': forms.Select(attrs={'class': 'form-control'}),
            'Classification_level': forms.Select(attrs={'class': 'form-control'}),
            'document_owner': forms.Select(attrs={'class': 'form-control'}),
            'Recipient': forms.Select(attrs={'class': 'form-control'})
        }
