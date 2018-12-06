from django import forms
from django.forms import formset_factory
from .models import Projet, Client, Collaborateur, Equipe, Commande
from .models import RepartitionProjet, RDate, Pourcentage


class DatePrtForm(forms.ModelForm):

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


DateFormSet = formset_factory(DatePrtForm, extra=3)


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
        fields = ('projet', 'ref', 'charges', 'equipe', 'commentaire')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['projet'].queryset = Projet.objects.all()
        self.fields['equipe'].queryset = Equipe.objects.all()


class UpdateCommandeForm(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('projet', 'ref', 'charges',
                  'chargesRAF', 'equipe', 'commentaire')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chargesRAF'].label = "Charges reste à faire"
        self.fields['projet'].queryset = Projet.objects.all()
        self.fields['equipe'].queryset = Equipe.objects.all()


class PassCommandFromTaskForm(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('projet', 'ref', 'charges',
                  'date_commande', 'etablie', 'equipe', 'commentaire')
