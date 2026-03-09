from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    file = models.FileField(upload_to='documents/', verbose_name="Fichier")
    category = models.CharField(max_length=100, verbose_name="Catégorie", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    def __str__(self):
        return self.title
