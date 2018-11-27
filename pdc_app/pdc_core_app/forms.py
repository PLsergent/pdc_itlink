from django import forms
from .models import Client


class AjoutClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('nomCl',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nomCl'].label = "Nom client"
