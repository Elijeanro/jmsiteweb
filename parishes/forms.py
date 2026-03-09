from django import forms
from django.core.exceptions import ValidationError
from .models import Parish, Doyenne

class DoyenneForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier les doyennés.
    """
    class Meta:
        model = Doyenne
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du doyenné'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Le nom est obligatoire.")
        return name

class ParishForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier les paroisses.
    """
    class Meta:
        model = Parish
        fields = ['name', 'location', 'doyenne', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la paroisse'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Localisation/Quartier'
            }),
            'doyenne': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Le nom est obligatoire.")
        return name

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if not image.name.lower().endswith(tuple(valid_extensions)):
                raise ValidationError("Seules les images JPG, JPEG et PNG sont autorisées.")
        return image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'image':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
