from django import forms
from django.core.exceptions import ValidationError
from .models import Event, EventImage
from datetime import date

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'événement'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description de l\'événement',
                'rows': 4
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Le titre est obligatoire.")
        if Event.objects.filter(title=title).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Un événement avec ce titre existe déjà.")
        return title

    def clean_date(self):
        date_event = self.cleaned_data.get('date')
        if date_event and date_event < date.today():
            raise ValidationError("La date ne peut pas être dans le passé.")
        return date_event

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class EventImageForm(forms.Form):
    images = MultipleFileField(required=False)
    def clean_images(self):
        images = self.cleaned_data.get('images')
        for image in images:
            if image.content_type not in ['image/jpeg', 'image/png']:
                raise ValidationError("Seules les images JPEG et PNG sont autorisées.")
            if image.size > 5 * 1024 * 1024:  # Limite de 5MB
                raise ValidationError("Chaque image doit être inférieure à 5MB.")
        return images