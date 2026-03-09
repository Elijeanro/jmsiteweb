from django import forms
from django.core.exceptions import ValidationError
from .models import Histories, HistoryEntry

class HistoriesForm(forms.ModelForm):
    class Meta:
        model = Histories
        fields = ['title', 'base']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'historique'
            }),
            'base': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Le titre est obligatoire.")
        return title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['base'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class HistoryEntryForm(forms.ModelForm):
    class Meta:
        model = HistoryEntry
        fields = ['subtitle', 'content', 'date', 'image']
        widgets = {
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sous-titre de l\'entrée historique'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Contenu',
                'rows': 5
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

    def clean_subtitle(self):
        subtitle = self.cleaned_data.get('subtitle')
        if not subtitle:
            raise ValidationError("Le sous-titre est obligatoire.")
        return subtitle

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

class MultipleHistoryEntryForm(forms.Form):
    form_count = forms.IntegerField(widget=forms.HiddenInput(), initial=1)


from django import forms
from django.core.exceptions import ValidationError
from .models import HistoryEntry

class SimpleHistoryEntryForm(forms.ModelForm):
    class Meta:
        model = HistoryEntry
        fields = ['subtitle', 'content', 'date', 'image']
        widgets = {
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sous-titre'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_subtitle(self):
        subtitle = self.cleaned_data.get('subtitle')
        if not subtitle:
            raise ValidationError("Le sous-titre est obligatoire.")
        return subtitle
