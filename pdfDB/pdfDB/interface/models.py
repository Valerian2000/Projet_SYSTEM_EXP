from django.db import models

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nomf

class Etudiant(models.Model):
    annee = models.CharField(max_length=20)
    ecole = models.CharField(max_length=100)
    classe = models.CharField(max_length=50)
    eleve = models.CharField(max_length=100)
    pourcentage = models.FloatField()