from django import forms
from django.core.exceptions import ValidationError
from .models import FaustineContent

class FaustineContentForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier le contenu sur Sainte Faustine.
    """

    class Meta:
        model = FaustineContent
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du contenu'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Contenu',
                'rows': 5
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

    def clean_title(self):
        """
        Valide que le titre n'est pas vide.
        """
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Le titre est obligatoire.")
        return title

    def clean_image(self):
        """
        Valide que l'image téléchargée est bien une image.
        """
        image = self.cleaned_data.get('image')
        if image:
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if not image.name.lower().endswith(tuple(valid_extensions)):
                raise ValidationError("Seules les images JPG, JPEG et PNG sont autorisées.")
        return image

    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire avec des classes CSS pour Bootstrap.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'image':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
