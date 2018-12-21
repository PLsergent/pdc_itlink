from django.test import TestCase
from pdc_core_app.models import Equipe, Collaborateur, Client, Projet


class EquipeTest(TestCase):

    def create_equipe(self, nom="PyWe"):
        return Equipe.objects.create(nomE=nom)

    def test_equipe_create(self):
        equipe = self.create_equipe()
        self.assertTrue(isinstance(equipe, Equipe))
        self.assertEqual(equipe.__str__(), equipe.get_nomE_display())


class ProjetTest(TestCase):
    equipe = Equipe.objects.create(nomE="PyWe")
    rdp = Collaborateur.objects.get(trigrammeC='AGE')
    clt = Client.objects.create(nomCl="Test_itlink")

    def create_projet(self, nom_projet="Test_projet",
                      RdP=rdp, RT=rdp, client=clt):
        return Projet.objects.create(nomP=nom_projet,
                                     RdP=RdP,
                                     RT=RT,
                                     client=client
                                     )

    def test_projet_create(self):
        projet = self.create_projet()
        self.assertTrue(isinstance(projet, Projet))
        self.assertEqual(projet.__str__(),
                         f'{projet.nomP}, '
                         f'{projet.client.nomCl}, '
                         f'RdP: {projet.RdP.trigrammeC}')
