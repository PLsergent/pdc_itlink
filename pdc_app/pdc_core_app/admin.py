from django.contrib import admin
from .models import RepartitionActivite, RepartitionProjet, Commande, Projet
from .models import Activite, Client, Collaborateur, Responsable_E, Equipe
from .models import RDate


class RepartitionProjetAdmin(admin.ModelAdmin):
    ordering = ['collaborateur']
    list_display = ('commande', 'collaborateur')


admin.site.register(RepartitionProjet, RepartitionProjetAdmin)


class RepartitionActiviteAdmin(admin.ModelAdmin):
    ordering = ['collaborateur']
    list_display = ('activite', 'collaborateur')


admin.site.register(RepartitionActivite, RepartitionActiviteAdmin)


class CommandeAdmin(admin.ModelAdmin):
    ordering = ['projet']
    list_display = ('projet', 'equipe', 'date_commande', 'charges', 'ref',
                    'etablie')


admin.site.register(Commande, CommandeAdmin)


class ProjetAdmin(admin.ModelAdmin):
    ordering = ['client']
    list_display = ('nomP', 'client', 'RdP', 'RT')


admin.site.register(Projet, ProjetAdmin)


class ActiviteAdmin(admin.ModelAdmin):
    ordering = ['nomAct']
    list_display = ('nomAct',)


admin.site.register(Activite, ActiviteAdmin)


class ClientAdmin(admin.ModelAdmin):
    ordering = ['nomCl']
    list_display = ('nomCl',)


admin.site.register(Client, ClientAdmin)


class CollaborateurAdmin(admin.ModelAdmin):
    ordering = ['equipe']
    list_display = ('trigrammeC', 'nomC', 'prenomC', 'role', 'equipe')


admin.site.register(Collaborateur, CollaborateurAdmin)


class EquipeAdmin(admin.ModelAdmin):
    ordering = ['nomE']
    list_display = ('nomE',)


admin.site.register(Equipe, EquipeAdmin)


class Responsable_EAdmin(admin.ModelAdmin):
    ordering = ['equipe']
    list_display = ('RdE', 'equipe')


admin.site.register(Responsable_E, Responsable_EAdmin)


class RDateAdmin(admin.ModelAdmin):
    ordering = ['month']
    list_display = ('month', 'pourcentage')


admin.site.register(RDate, RDateAdmin)
