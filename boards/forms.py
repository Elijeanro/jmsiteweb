from django import forms
from django.core.exceptions import ValidationError
from .models import Member, MemberPosition, Mandate, Board, BoardMembership, BoardType

class BoardTypeForm(forms.ModelForm):
    class Meta:
        model = BoardType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du type de bureau'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du type de bureau'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Le nom du type de bureau est obligatoire.")
        return name

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'gender', 'position', 'photo', 'bio', 'email', 'phone', 'parish', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'parish': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if not any(photo.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError("Seules les images JPG, JPEG et PNG sont autorisées.")
        return photo

class MemberPositionForm(forms.ModelForm):
    class Meta:
        model = MemberPosition
        fields = ['name', 'description', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MandateForm(forms.ModelForm):
    class Meta:
        model = Mandate
        fields = ['member', 'start_date', 'end_date', 'is_current', 'description', 'board_type']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'board_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_current = cleaned_data.get('is_current')
        board_type = cleaned_data.get('board_type')
        member = cleaned_data.get('member')

        if start_date and end_date and start_date > end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")

        if end_date and is_current:
            raise ValidationError("Un mandat avec une date de fin ne peut pas être marqué comme actuel.")

        # Vérification des règles de non-cumul
        if is_current and member:
            # Règle 1: Un membre diocésain ne peut pas être dans un autre bureau
            if board_type == 'diocesan':
                current_mandates = Mandate.objects.filter(
                    member=member,
                    is_current=True
                ).exclude(pk=self.instance.pk if self.instance else None)

                for mandate in current_mandates:
                    if mandate.board_type != 'diocesan':
                        raise ValidationError(
                            "Un membre du bureau diocésain ne peut pas être membre d'un autre type de bureau."
                        )

            # Règle 2: Un membre paroissial ne peut être que dans son doyenné
            elif board_type == 'parish':
                current_decanal_mandates = Mandate.objects.filter(
                    member=member,
                    is_current=True,
                    board_type='decanal'
                ).exclude(pk=self.instance.pk if self.instance else None)

                for mandate in current_decanal_mandates:
                    parish = member.parish
                    if parish and parish.doyenne:
                        if hasattr(mandate, 'doyenne') and mandate.doyenne != parish.doyenne:
                            raise ValidationError(
                                "Un membre de bureau paroissial ne peut être que dans son propre doyenné."
                            )

        return cleaned_data

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'board_type', 'doyenne', 'parish', 'start_date', 'end_date', 'is_current']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'board_type': forms.Select(attrs={'class': 'form-select'}),
            'doyenne': forms.Select(attrs={'class': 'form-select'}),
            'parish': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        board_type = cleaned_data.get('board_type')
        doyenne = cleaned_data.get('doyenne')
        parish = cleaned_data.get('parish')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_current = cleaned_data.get('is_current')

        # Validation des dates
        if start_date and end_date and start_date > end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")

        if end_date and is_current:
            raise ValidationError("Un bureau avec une date de fin ne peut pas être marqué comme actif.")

        # Validation des affiliations
        if board_type == 'decanal' and not doyenne:
            raise ValidationError("Veuillez sélectionner un doyenné pour un bureau décanal.")

        if board_type == 'parish' and not parish:
            raise ValidationError("Veuillez sélectionner une paroisse pour un bureau paroissial.")

        if board_type != 'decanal' and doyenne:
            self.add_error('doyenne', "Le doyenné ne doit être sélectionné que pour un bureau décanal.")

        if board_type != 'parish' and parish:
            self.add_error('parish', "La paroisse ne doit être sélectionnée que pour un bureau paroissial.")

        return cleaned_data

class BoardMembershipForm(forms.ModelForm):
    class Meta:
        model = BoardMembership
        fields = ['board', 'member', 'position', 'mandate']
        widgets = {
            'board': forms.Select(attrs={'class': 'form-select'}),
            'member': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'mandate': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['mandate'].queryset = Mandate.objects.filter(
                member=self.instance.member,
                board_type=self.instance.board.board_type
            )

    def clean(self):
        cleaned_data = super().clean()
        board = cleaned_data.get('board')
        member = cleaned_data.get('member')
        mandate = cleaned_data.get('mandate')

        if board and member and mandate:
            if mandate.board_type != board.board_type:
                raise ValidationError("Le type de mandat doit correspondre au type de bureau.")

            if mandate.member != member:
                raise ValidationError("Le mandat doit être associé au même membre.")

        return cleaned_data
