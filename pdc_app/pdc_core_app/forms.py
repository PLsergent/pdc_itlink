from django import forms
from .models import Projet, Client, Collaborateur


class AjoutProjetForm(forms.ModelForm):

    class Meta:
        model = Projet
        fields = ('nomP', 'RdP', 'RT', 'client')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nomP'].label = "Nom projet"
        self.fields['client'].queryset = Client.objects.none()
        self.fields['RdP'].queryset = Collaborateur.objects.none()
        self.fields['RT'].queryset = Collaborateur.objects.none()


class AjoutClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('nomCl',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nomCl'].label = "Nom client"
