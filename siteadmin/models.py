from django.db import models
from django.contrib.auth.models import User

class AdminActivityLog(models.Model):
    """
    Modèle pour enregistrer les activités des administrateurs.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    action = models.CharField(max_length=255, verbose_name="Action")
    model_name = models.CharField(max_length=100, verbose_name="Modèle concerné")
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="ID de l'objet")
    details = models.TextField(blank=True, verbose_name="Détails")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure")

    class Meta:
        verbose_name = "Log d'activité admin"
        verbose_name_plural = "Logs d'activité admin"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.created_at}"

class SiteConfiguration(models.Model):
    """
    Modèle pour stocker les configurations spécifiques du site.
    """
    site_name = models.CharField(max_length=100, verbose_name="Nom du site", default="Association Jésus Miséricordieux")
    contact_email = models.EmailField(verbose_name="Email de contact")
    maintenance_mode = models.BooleanField(default=False, verbose_name="Mode maintenance")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configurations du site"

    def __str__(self):
        return self.site_name
