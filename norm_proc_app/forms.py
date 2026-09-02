from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import Norms, Procedures

User = get_user_model()

class NormForm(ModelForm):
    class Meta:
        model = Norms
        fields = ['title', 'file', 'content', 'legal_basis', 'document_type', 'responsible_department']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'documentFile'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'legal_basis': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'responsible_department': forms.Select(attrs={'class': 'form-control'})
        }

class ProcedureForm(ModelForm):
    class Meta:
        model = Procedures
        fields = ['title', 'content', 'steps', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'steps': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
