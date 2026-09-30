from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import BaseDocument

User = get_user_model()

class DocumentForm(ModelForm):
    class Meta:
        model = BaseDocument
        fields = ['title', 'file', 'Description', 'document_type', 'Recipient', 'Classification_level']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'documentFile'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'Recipient': forms.Select(attrs={'class': 'form-control'}),
            'Classification_level': forms.Select(attrs={'class': 'form-control'})
        }
