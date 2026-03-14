from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Program,
    ProgramContentFile,
    ProgramContentSchedule,
    ProgramContentScheduleList,
)


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Titre du programme",
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 4,
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Le titre est obligatoire.")
        return title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_active':
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProgramContentFileForm(forms.ModelForm):
    class Meta:
        model = ProgramContentFile
        fields = ['program', 'file', 'label', 'end_date']
        widgets = {
            'program': forms.Select(attrs={
                'class': 'form-select',
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
            'label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Libellé du fichier',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.webp']
            if not file.name.lower().endswith(tuple(valid_extensions)):
                raise ValidationError("Seuls les fichiers PDF et images (JPG, PNG, WEBP) sont autorisés.")
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in {'file', 'program'}:
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProgramContentScheduleForm(forms.ModelForm):
    class Meta:
        model = ProgramContentSchedule
        fields = ['program', 'start_date', 'end_date', 'subtitle']
        widgets = {
            'program': forms.Select(attrs={
                'class': 'form-select',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sous-titre',
            }),
        }

    def clean_start_date(self):
        value = self.cleaned_data.get('start_date')
        if not value:
            raise ValidationError("La date de début est obligatoire.")
        return value


class ProgramContentScheduleListForm(forms.ModelForm):
    class Meta:
        model = ProgramContentScheduleList
        fields = ['schedule', 'start_time', 'end_time', 'description']
        widgets = {
            'schedule': forms.Select(attrs={
                'class': 'form-select',
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
        }

    def clean_start_time(self):
        value = self.cleaned_data.get('start_time')
        if not value:
            raise ValidationError("L'heure de début est obligatoire.")
        return value
