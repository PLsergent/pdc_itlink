from django import forms
from django.forms import formset_factory
from django.forms import BaseFormSet
from .models import Projet, Client, Collaborateur, Equipe, Commande, Activite
from .models import RepartitionProjet, RDate, Pourcentage, RepartitionActivite
from django.contrib.auth.models import User


# =============================== FORMSET ====================================
class DatePrctForm(forms.ModelForm):

    class Meta:
        model = RDate
        fields = ('month', 'pourcentage')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pourcentage'].queryset = Pourcentage.objects.all()


class AffectationCollabProjetForm(forms.ModelForm):

    class Meta:
        model = RepartitionProjet
        fields = ('commande', 'collaborateur')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['commande'].queryset = Commande.objects.all()
        self.fields['collaborateur'].queryset = Collaborateur.objects.all()


class AffectationCollabActForm(forms.ModelForm):

    class Meta:
        model = RepartitionActivite
        fields = ('activite', 'collaborateur')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activite'].queryset = Activite.objects.all()
        self.fields['collaborateur'].queryset = Collaborateur.objects.all()


DateFormSet = formset_factory(DatePrctForm, formset=BaseFormSet)


# =============================================================================
class AjoutProjetForm(forms.ModelForm):

    class Meta:
        model = Projet
        fields = ('nomP', 'RdP', 'RT', 'client')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nomP'].label = "Nom projet"
        self.fields['client'].queryset = Client.objects.all()
        self.fields['RdP'].queryset = Collaborateur.objects.filter(role='RdP')
        self.fields['RT'].queryset = Collaborateur.objects.all()


class AjoutClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('nomCl',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nomCl'].label = "Nom client"


class AjoutCollabForm(forms.ModelForm):

    class Meta:
        model = Collaborateur
        fields = ('trigrammeC', 'nomC', 'prenomC', 'role', 'equipe')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['equipe'].queryset = Equipe.objects.all()
        self.fields['trigrammeC'].label = "Trigramme"
        self.fields['nomC'].label = "Nom"
        self.fields['prenomC'].label = "Prénom"
        self.fields['role'].label = "Rôle"


class PasserCommandeForm(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('projet', 'ref', 'charges',
                  'date_commande', 'etablie', 'equipe', 'commentaire')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['projet'].queryset = Projet.objects.all()
        self.fields['equipe'].queryset = Equipe.objects.all()
        self.fields['date_commande'].label = "Date"
        self.fields['etablie'].initial = True


class NouvelleTacheProbableForm(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('projet', 'ref', 'charges', 'date_commande',
                  'odds', 'equipe', 'commentaire')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['projet'].queryset = Projet.objects.all()
        self.fields['equipe'].queryset = Equipe.objects.all()
        self.fields['odds'].label = "Probabilité"
        self.fields['date_commande'].label = "Date"


# =============================================================================
class UpdateCommandeForm(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('projet', 'ref', 'charges',
                  'chargesRAF', 'etablie', 'odds', 'equipe', 'commentaire')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chargesRAF'].label = "Charges reste à faire"
        self.fields['odds'].label = "Probabilité"
        self.fields['projet'].queryset = Projet.objects.all()
        self.fields['equipe'].queryset = Equipe.objects.all()


class PassCommandFromTaskForm(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('projet', 'ref', 'charges',
                  'date_commande', 'etablie', 'equipe', 'commentaire')


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined', 'password']
