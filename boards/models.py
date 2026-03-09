from django.db import models
from django.core.exceptions import ValidationError
from parishes.models import Parish, Doyenne

class BoardType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Type de bureau")
    description = models.TextField(verbose_name="Description", blank=True)

    class Meta:
        verbose_name = "Type de bureau"
        verbose_name_plural = "Types de bureau"

    def __str__(self):
        return self.name

class MemberPosition(models.Model):
    name = models.CharField(max_length=100, verbose_name="Poste", unique=True)
    description = models.TextField(verbose_name="Description", help_text="Description du poste")
    order = models.PositiveIntegerField(
        verbose_name="Ordre d'affichage",
        default=0,
        help_text="Définit l'ordre d'affichage des postes"
    )

    class Meta:
        verbose_name = "Poste"
        verbose_name_plural = "Postes"
        ordering = ['order']

    def __str__(self):
        return self.name

class Member(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Genre")
    position = models.ForeignKey(
        MemberPosition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Poste"
    )
    photo = models.ImageField(
        upload_to='members/photos/',
        verbose_name="Photo",
        blank=True,
        null=True
    )
    bio = models.TextField(
        verbose_name="Biographie",
        blank=True,
        null=True,
        help_text="Brève biographie du membre"
    )
    email = models.EmailField(
        verbose_name="Email",
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
        blank=True,
        null=True
    )
    parish = models.ForeignKey(
        Parish,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Paroisse",
        related_name='members'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ['position__order', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Board(models.Model):
    BOARD_TYPES = [
        ('diocesan', 'Bureau Diocésain'),
        ('decanal', 'Bureau Décanal'),
        ('parish', 'Bureau Paroissial'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nom")
    board_type = models.CharField(
        max_length=20,
        choices=BOARD_TYPES,
        verbose_name="Type de bureau"
    )
    doyenne = models.ForeignKey(
        Doyenne,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Doyenné",
        help_text="À remplir uniquement pour les bureaux décanaux"
    )
    parish = models.ForeignKey(
        Parish,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Paroisse",
        help_text="À remplir uniquement pour les bureaux paroissiaux"
    )
    start_date = models.DateField(
        verbose_name="Date de début",
        null=True,
        blank=True
    )
    end_date = models.DateField(
        verbose_name="Date de fin",
        null=True,
        blank=True,
        help_text="Laisser vide si le bureau est toujours actif"
    )
    is_current = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Indique si ce bureau est actuellement actif"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    class Meta:
        verbose_name = "Bureau"
        verbose_name_plural = "Bureaux"
        ordering = ['-start_date', 'name']

    def __str__(self):
        return f"{self.get_board_type_display()} - {self.name}"

class Mandate(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        verbose_name="Membre",
        related_name='mandates'
    )
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(
        verbose_name="Date de fin",
        blank=True,
        null=True,
        help_text="Laisser vide si le mandat est toujours en cours"
    )
    is_current = models.BooleanField(
        default=True,
        verbose_name="Mandat actuel",
        help_text="Indique si ce mandat est actuellement en cours"
    )
    board_type = models.CharField(
        max_length=20,
        choices=Board.BOARD_TYPES,
        verbose_name="Type de bureau",
        help_text="Type de bureau pour ce mandat"
    )
    description = models.TextField(
        verbose_name="Description du mandat",
        blank=True,
        null=True,
        help_text="Description détaillée du mandat"
    )

    class Meta:
        verbose_name = "Mandat"
        verbose_name_plural = "Mandats"
        ordering = ['-start_date']

    def __str__(self):
        end = self.end_date.strftime("%Y") if self.end_date else "en cours"
        return f"{self.member} ({self.start_date.year} - {end})"

    def clean(self):
        from django.core.exceptions import ValidationError

        # Règle 1: Un membre diocésain ne peut pas être dans un autre bureau
        if self.is_current and self.board_type == 'diocesan':
            current_mandates = Mandate.objects.filter(
                member=self.member,
                is_current=True
            ).exclude(pk=self.pk)

            for mandate in current_mandates:
                if mandate.board_type != 'diocesan':
                    raise ValidationError({
                        'member': "Un membre du bureau diocésain ne peut pas être membre d'un autre type de bureau."
                    })

        # Règle 2: Un membre paroissial ne peut être que dans son doyenné
        elif self.is_current and self.board_type == 'parish':
            current_decanal_mandates = Mandate.objects.filter(
                member=self.member,
                is_current=True,
                board_type='decanal'
            ).exclude(pk=self.pk)

            for mandate in current_decanal_mandates:
                if self.member.parish and self.member.parish.doyenne:
                    if hasattr(mandate, 'doyenne') and mandate.doyenne != self.member.parish.doyenne:
                        raise ValidationError({
                            'member': "Un membre de bureau paroissial ne peut être que dans son propre doyenné."
                        })

class BoardMembership(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        verbose_name="Bureau"
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        verbose_name="Membre"
    )
    position = models.ForeignKey(
        MemberPosition,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Poste",
        related_name='board_memberships'
    )
    mandate = models.OneToOneField(
        Mandate,
        on_delete=models.CASCADE,
        verbose_name="Mandat",
        related_name='board_membership'
    )

    class Meta:
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"
        unique_together = ('board', 'member', 'position')

    def __str__(self):
        return f"{self.member} - {self.position} - {self.board}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.mandate.board_type != self.board.board_type:
            raise ValidationError("Le type de mandat doit correspondre au type de bureau.")

        if self.mandate.member != self.member:
            raise ValidationError("Le mandat doit être associé au même membre.")
