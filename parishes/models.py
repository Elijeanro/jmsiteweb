from django.db import models

class Doyenne(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom du Doyenné")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    def __str__(self):
        return self.name
    
class Parish(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom de la Paroisse")
    location = models.CharField(max_length=200, verbose_name="Localisation/Quartier")
    doyenne = models.ForeignKey(Doyenne, on_delete=models.CASCADE, related_name='parishes', verbose_name="Doyenné", blank=True, null=True)
    image = models.ImageField(upload_to='parishes/', verbose_name="Image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    def __str__(self):
        return self.name
