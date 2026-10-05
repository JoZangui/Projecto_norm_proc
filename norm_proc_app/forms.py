from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import BaseDocument

User = get_user_model()

class DocumentForm(ModelForm):
    class Meta:
        model = BaseDocument
        fields = [
            'title', # Adicionado para permitir a inserção do título do documento
            'file', # Adicionado para permitir o upload do arquivo do documento
            'description', # Adicionado para permitir a inserção da descrição do documento
            'document_type', # Adicionado para permitir a seleção do tipo de documento (Norma, Procedimento, Política, Regulamento, Manual, Guia, SOP)
            'classification_level', # Adicionado para permitir a seleção do nível de classificação do documento (Público, Interno, Confidencial, Restrito)
            'created_at', # Adicionado para permitir a seleção da data de criação do documento
            'reviewed_by', # Adicionado para permitir a seleção do revisor do documento
            'approved_by', # Adicionado para permitir a seleção do aprovador do documento
            'document_owner', # Adicionado para permitir a seleção do departamento proprietário do documento
            'recipient', # Adicionado para permitir a seleção do destinatário do documento (Se for para todos só precisamos selecionar a opção "Todos")
            'code', # Adicionado para permitir a inserção do código do documento
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'documentFile'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'classification_level': forms.Select(attrs={'class': 'form-control'}),
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reviewed_by': forms.Select(attrs={'class': 'form-control'}),
            'approved_by': forms.Select(attrs={'class': 'form-control'}),
            'document_owner': forms.Select(attrs={'class': 'form-control'}),
            'recipient': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }
