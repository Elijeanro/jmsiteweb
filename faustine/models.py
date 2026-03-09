from django.db import models

class FaustineContent(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    image = models.ImageField(upload_to='faustine/', verbose_name="Image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    def __str__(self):
        return self.title
