from django.db import models
from month.models import MonthField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from datetime import datetime as dt
import reversion


class Equipe(models.Model):
    idEquipe = models.AutoField(primary_key=True)
    EQUIPE = (
        ('PyWe', 'PythonWeb'),
        ('PyQt', 'PythonQt'),
        ('CPQt', 'CPlusQt')
    )
    nomE = models.CharField(max_length=4, choices=EQUIPE)

    def __str__(self):
        return f'{self.get_nomE_display()}'


@reversion.register
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

    def __str__(self):
        return f'{self.trigrammeC}, {self.nomC}, {self.get_role_display()}'


@reversion.register(follow=["RdE"])
class Responsable_E(models.Model):
    idRespE = models.AutoField(primary_key=True)
    RdE = models.OneToOneField(Collaborateur, on_delete=models.CASCADE)
    equipe = models.OneToOneField(Equipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.RdE.trigrammeC}'


@reversion.register
class Client(models.Model):
    idClient = models.AutoField(primary_key=True)
    nomCl = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nomCl}'


@reversion.register(follow=["RdP", "RT", "client"])
class Projet(models.Model):
    idProjet = models.AutoField(primary_key=True)
    nomP = models.CharField(max_length=50)
    RdP = models.ForeignKey(Collaborateur, on_delete=models.CASCADE,
                            related_name="respP")
    RT = models.ForeignKey(Collaborateur, on_delete=models.CASCADE,
                           related_name="respT")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nomP}, {self.client.nomCl}'


@reversion.register(follow=["projet"])
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
    odds = models.PositiveIntegerField(default=100)
    commentaire = models.CharField(max_length=200, blank=True)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.projet.nomP}, ' + \
            f'{self.projet.client.nomCl}, ' + \
            f'{self.ref}'

    def save(self, *args, **kwargs):
        if not self.chargesRAF:
            self.chargesRAF = self.charges
        if not self.etablie:
            self.etablie = False
        if not self.date_commande:
            self.date_commande = dt.today()
        if not self.odds:
            self.odds = 100
        super(Commande, self).save(*args, **kwargs)


@reversion.register()
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

    def __str__(self):
        return f'{self.get_nomAct_display()}'


class Pourcentage(models.Model):
    pourcentage = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
    )

    def __str__(self):
        return f'{self.pourcentage}'


class RDate(models.Model):
    month = MonthField("Month Value")
    pourcentage = models.ForeignKey(Pourcentage, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.month}, {self.pourcentage.pourcentage}'


@reversion.register(follow=["activite", "collaborateur"])
class RepartitionActivite(models.Model):
    idRA = models.AutoField(primary_key=True)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    collaborateur = models.ForeignKey(Collaborateur, on_delete=models.CASCADE)
    list_R = models.ManyToManyField(RDate)

    def __str__(self):
        return f'{self.activite.get_nomAct_display()}, ' + \
            f'{self.collaborateur.nomC}'


@reversion.register(follow=["commande", "collaborateur"])
class RepartitionProjet(models.Model):
    idRP = models.AutoField(primary_key=True)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    collaborateur = models.ForeignKey(Collaborateur, on_delete=models.CASCADE)
    list_R = models.ManyToManyField(RDate)

    def __str__(self):
        return f'{self.commande.projet.nomP}, ' + \
            f'{self.commande.ref}, ' + \
            f'{self.collaborateur.nomC}'


class History(models.Model):
    date = models.DateTimeField(
        db_index=True,
        verbose_name=("date created"),
        help_text="The date and time this revision was created.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=("user"),
        help_text="The user who created this revision.",
    )
    model = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="Content type of the model under version control.",
    )
    object_repr = models.TextField(
        help_text="A string representation of the object.",
    )
    comment = models.TextField(
        blank=True,
        verbose_name=("comment"),
        help_text="A text comment on this revision.",
    )
