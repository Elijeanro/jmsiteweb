from django.db import models
from parishes.models import Parish


class Histories(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    base = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name='histories', verbose_name="Base/Paroisse", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    def __str__(self):
        return f"{self.title}"
    
class HistoryEntry(models.Model):
    title = models.ForeignKey(Histories, on_delete=models.CASCADE, related_name='entries', verbose_name="Historique")
    subtitle = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    date = models.DateField(verbose_name="Date de l'événement")
    image = models.ImageField(upload_to='history/', verbose_name="Image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    def __str__(self):
        return f"{self.title} | {self.subtitle} ({self.date})"
