from django.db import models
from django.core.validators import MinValueValidator
import json


class Equipe(models.Model):
    idEquipe = models.AutoField(primary_key=True)
    EQUIPE = (
        ('PyWe', 'PythonWeb'),
        ('PyQt', 'PythonQt'),
        ('CPQt', 'CPlusQt')
    )
    nomE = models.CharField(max_length=4, choices=EQUIPE)


class Collaborateur(models.Model):
    trigrammeC = models.CharField(max_length=3, primary_key=True)
    nomC = models.CharField(max_length=50)
    prenomC = models.CharField(max_length=50)
    ROLE = (
        ('RdP', 'Responsable de projet'),
        ('IE', 'Ingénieur étude'),
        ('Stg', 'Stagiaire')
    )
    role = models.CharField(max_length=3, choices=ROLE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)


class Responsable_E(models.Model):
    idRespE = models.AutoField(primary_key=True)
    RdE = models.OneToOneField(Collaborateur, on_delete=models.CASCADE)
    equipe = models.OneToOneField(Equipe, on_delete=models.CASCADE)


class Client(models.Model):
    idClient = models.AutoField(primary_key=True)
    nomCl = models.CharField(max_length=50)


class Projet(models.Model):
    idProjet = models.AutoField(primary_key=True)
    nomP = models.CharField(max_length=50)
    RdP = models.ForeignKey(Collaborateur, on_delete=models.CASCADE,
                            related_name="respP")
    RT = models.ForeignKey(Collaborateur, on_delete=models.CASCADE,
                           related_name="respT")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Commande(models.Model):
    idCom = models.AutoField(primary_key=True)
    ref = models.CharField(blank=True, max_length=100)
    charges = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )
    chargesRAF = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )
    date_commande = models.DateField()
    etablie = models.BooleanField(default=False)
    commentaire = models.CharField(max_length=200)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)


class Activite(models.Model):
    idAct = models.AutoField(primary_key=True)
    ACTIVITE = (
        ('c', 'Conges'),
        ('m', 'Maladie'),
        ('a', 'Absence'),
        ('d', 'Deplacement'),
        ('rao', 'RAO'),
        ('alt', 'Alternance'),
        ('au', 'Autres')
    )
    nomAct = models.CharField(max_length=3, choices=ACTIVITE)


class RepartitionActivite(models.Model):
    idRA = models.AutoField(primary_key=True)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    collaborateur = models.ForeignKey(Collaborateur, on_delete=models.CASCADE)
    list_RA = models.CharField(max_length=1000)

    def set_list(self, x):
        self.list_RA = json.dumps(x)

    def get_list(self, x):
        self.list_RA = json.loads(x)


class RepartitionProjet(models.Model):
    idRP = models.AutoField(primary_key=True)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    collaborateur = models.ForeignKey(Collaborateur, on_delete=models.CASCADE)
    list_R = models.CharField(max_length=1000)

    def set_list(self, x):
        self.list_RA = json.dumps(x)

    def get_list(self, x):
        self.list_RA = json.loads(x)
