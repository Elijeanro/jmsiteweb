from django import forms
from django.core.exceptions import ValidationError
from .models import Document

class DocumentForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier des documents.
    """

    class Meta:
        model = Document
        fields = ['title', 'file', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du document'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_file(self):
        """
        Valide que le fichier téléchargé est un PDF.
        """
        file = self.cleaned_data.get('file')
        if file:
            valid_extensions = ['.pdf']
            if not file.name.lower().endswith(tuple(valid_extensions)):
                raise ValidationError("Seuls les fichiers PDF sont autorisés.")
        return file

    def clean_title(self):
        """
        Valide que le titre n'est pas vide.
        """
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Le titre est obligatoire.")
        return title

    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire avec des classes CSS pour Bootstrap.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'file':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
