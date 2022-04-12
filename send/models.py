from django.db import models

# Create your models here.

class Candidat(models.Model):
    telephone = models.CharField(max_length=255)
    telephone_pere = models.CharField(max_length=255, null=True, blank=True)
    telephone_mere = models.CharField(max_length=255, null=True, blank=True)
    nom = models.CharField(max_length=255)
    concours = models.CharField(max_length=255)
    etablissement = models.CharField(max_length=255)
    salle = models.CharField(max_length=255)
    table = models.CharField(max_length=255)
    date_exam = models.DateField()
    date_envoi = models.CharField(max_length=255, blank=True, null=True)
    go = models.BooleanField(default=False)
    status_code = models.CharField(max_length=255, blank=True, null=True)
    status_msg = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{}-{}-{}".format(self.telephone, self.nom, self.concours)

    class Meta:
       verbose_name = 'Candidat'
       verbose_name_plural = 'Candidats'
