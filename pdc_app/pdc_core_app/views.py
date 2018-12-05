from datetime import datetime as datet, date
from dateutil import relativedelta as rd
from workdays import networkdays
import calendar
from vanilla import DeleteView
import month

from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse

from .models import RepartitionProjet, RepartitionActivite, Commande
from .models import Collaborateur, Responsable_E, Projet, Client, RDate
from .models import Pourcentage

from .forms import AjoutClientForm, AjoutCollabForm, PasserCommandeForm
from .forms import AjoutProjetForm, NouvelleTacheProbableForm
from .forms import UpdateCommandeForm, PassCommandFromTaskForm
from .forms import AffectationCollabProjetForm


def get_month(number_month):
    lmd = []
    lm = []
    for i in range(0, number_month):
        date_month_after = datet.now() + rd.relativedelta(months=i)
        lmd.append((date_month_after.month, date_month_after.year))
        lm.append(month.Month(date_month_after.year, date_month_after.month))
    return lm, lmd


def get_repartition(type):
    list_month_display = []
    list_month = []
    all = []
    list_month, list_month_display = get_month(18)
    if type == 'P':
        repartitions = RepartitionProjet.objects.all()
    elif type == 'A':
        repartitions = RepartitionActivite.objects.all()
    else:
        return None
    # Information : colonnes de gauche
    for rp in repartitions:
        list = []
        if type == 'P':
            list.extend((rp.commande.idCom, rp.commande.equipe.nomE,
                         rp.collaborateur.trigrammeC,
                         rp.commande.projet.client.nomCl,
                         rp.commande.projet.nomP, rp.commande.ref,
                         rp.commande.projet.RdP.trigrammeC,
                         rp.commande.projet.RT.trigrammeC,
                         rp.commande.etablie))
        elif type == 'A':
            list.extend((rp.collaborateur.equipe.nomE,
                         rp.collaborateur.trigrammeC,
                         rp.activite))
        else:
            return None
        # Création d'une nouvelle liste pour récupérer les mois/année car le
        # format est différent que pour l'affichage. On récupère tous les
        # mois/année pour regarder si le mois courant est présent dans l'un
        # des pourcentages présent
        list_month_repartition = []
        for some in rp.list_R.filter(month__gte=datet.now()):
            list_month_repartition.append(some.month)
        # Pour chaque mois, si un pourcentage a été donné pour ce mois ci,
        # alors on récupère l'index de la date en question afin de récupérer
        # le pourcentage affecté à cette date
        for lm in list_month:
            if lm in list_month_repartition:
                i = list_month_repartition.index(lm)
                pourc_collab = rp.list_R.filter(
                    month__gte=datet.now())[i].pourcentage.pourcentage
                list.append(pourc_collab)
            else:
                list.append(0)
        # Ajout des charges et charges RAF
        if type == 'P':
            list.extend((rp.commande.chargesRAF,
                         assigned_charges(rp.commande)))
        all.append(list)
    return list_month, list_month_display, all


def assigned_charges(cmd):
    list_month, list_month_display = get_month(18)
    repartition_projet = RepartitionProjet.objects.filter(commande=cmd)
    sum_list = []
    for rp in repartition_projet:
        list_month_repartition = []
        for some in rp.list_R.filter(month__gte=datet.now()):
            list_month_repartition.append(some.month)

        for lm in list_month:
            if lm in list_month_repartition:
                i = list_month_repartition.index(lm)
                pourc_collab = rp.list_R.filter(
                    month__gte=datet.now())[i].pourcentage.pourcentage
                sum_list.append(pourc_collab/100)
    sum_rp = sum(sum_list)
    days_list = []
    for lm in list_month_display:
        start_date = date(lm[1], lm[0], 1)
        end_date = date(lm[1], lm[0],
                        calendar.monthrange(lm[1], lm[0])[1])
        days_list.append(networkdays(start_date, end_date))
    days = sum(days_list)
    return "%.1f" % (sum_rp * days / len(list_month_display))


# get_repartition_without_information, used in collaborateurs()
def get_repartition_wo_inf(type, collab):
    list_month, list_month_display = get_month(18)

    if type == 'P':
        repartition = RepartitionProjet.objects.filter(collaborateur=collab)
    elif type == 'A':
        repartition = RepartitionActivite.objects.filter(collaborateur=collab)
    else:
        return None

    pourcentages = []
    for rp in repartition:
        listP = []
        list_month_repartition = []
        for some in rp.list_R.filter(month__gte=datet.now()):
            list_month_repartition.append(some.month)

        for lm in list_month:
            if lm in list_month_repartition:
                i = list_month_repartition.index(lm)
                pourc_collab = rp.list_R.filter(
                    month__gte=datet.now())[i].pourcentage.pourcentage
                listP.append(pourc_collab)
            else:
                listP.append(0)
        pourcentages.append(listP)
    return pourcentages


def index(request):
    return render(request, 'pdc_core_app/index.html')


def projets(request):
    page_title = 'Affectations projets'
    list_month_display = []
    list_month = []
    all = []
    list_month, list_month_display, all = get_repartition('P')
    return render(request, 'pdc_core_app/projets.html',
                  {'page_title': page_title,
                   'list_month_display': list_month_display,
                   'all': all})


def collaborateurs(request):
    page_title = 'Collaborateurs'
    list_month_display = []
    list_month = []
    # Liste finale (all) contenant des listes, chaque liste contenant les
    # informations relative à un collaborateur
    all = []
    list_month, list_month_display = get_month(18)
    collaborateurs = Collaborateur.objects.all()
    # Récupération de tous les collaborateurs

    # Pour chaque collaborateur
    for collab in collaborateurs:
        # La list qui contient les informations relative à un seul collab
        # incluant les pourcentages qui sont ajoutés plus bas
        list = []
        rde = Responsable_E.objects.filter(equipe=collab.equipe)
        if rde:
            list.extend((collab.equipe.nomE, collab.trigrammeC, rde[0]))
        else:
            list.extend((collab.equipe.nomE, collab.trigrammeC, 'XXX'))
    # Dans la liste pourcentagesP on va stocker des listes, chaque liste
    # correspond aux pourcentages par mois d'un projet
        pourcentagesP = get_repartition_wo_inf('P', collab)
    # De même pour les activité, on fait une liste des pourcentages par
    # activité et on les stocks dans la liste pourcentagesA
        pourcentagesA = get_repartition_wo_inf('A', collab)
        pourcentages = pourcentagesP + pourcentagesA
    # Maintenant on a donc une liste de liste contenant les pourcentages par
    # projet et par activité. Ainsi on peut faire la somme de tous les éléments
    # de même rang pour avoir la somme des pourcentages par mois.
        for i in range(0, len(list_month)):
            somme = 0
            for p in pourcentages:
                somme += p[i]
            list.append(somme)
        all.append(list)

    return render(request, 'pdc_core_app/collaborateurs.html',
                  {'page_title': page_title,
                   'list_month_display': list_month_display,
                   'all': all})


def commandes(request):
    page_title = 'Commandes'
    all = []
    commandes = Commande.objects.all()

    for cmd in commandes:
        list = []
        if cmd.etablie is True:
            list.extend((cmd.idCom, cmd.equipe.nomE, cmd.date_commande,
                         cmd.projet.client.nomCl, cmd.projet.nomP,
                         cmd.projet.RdP.trigrammeC, cmd.charges, cmd.ref,
                         cmd.etablie, cmd.commentaire))
        if list:
            all.append(list)

    return render(request, 'pdc_core_app/commandes.html',
                  {'page_title': page_title,
                   'all': all})


def autres(request):
    page_title = 'Autres'
    list_month_display = []
    list_month = []
    all = []
    list_month, list_month_display, all = get_repartition('A')
    return render(request, 'pdc_core_app/autres.html',
                  {'page_title': page_title,
                   'list_month_display': list_month_display,
                   'all': all})


def data(request):
    page_title = 'Données'
    projets = Projet.objects.all()
    clients = Client.objects.all()
    collabs = Collaborateur.objects.all()
    commandes = Commande.objects.filter(etablie=False)

    return render(request, 'pdc_core_app/data.html',
                  {'page_title': page_title,
                   'projets': projets,
                   'clients': clients,
                   'collabs': collabs,
                   'commandes': commandes})


class AjoutProjet(SuccessMessageMixin, CreateView):
    model = Projet
    form_class = AjoutProjetForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "Le projet %(projet) aa été créé avec succès."

    def get_context_data(self, **args):
        context = super(CreateView, self).get_context_data(**args)
        context['page_title'] = 'Ajout projet'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            projet=self.object.nomP,
        )

    def form_valid(self, form):
        exist = Projet.objects.filter(nomP=form.cleaned_data['nomP'],
                                      client=form.cleaned_data['client'])
        if exist:
            form.add_error('nomP', 'This name already exist')
            return self.form_invalid(form)
        return super(AjoutProjet, self).form_valid(form)


class AjoutClient(SuccessMessageMixin, CreateView):
    model = Client
    form_class = AjoutClientForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('data')
    success_message = "Le client %(client) aa été créé avec succès."

    def get_context_data(self, **args):
        context = super(CreateView, self).get_context_data(**args)
        context['page_title'] = 'Ajout client'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            client=self.object.nomCl,
        )

    def form_valid(self, form):
        exist = Client.objects.filter(nomCl=form.cleaned_data['nomCl'])
        if exist:
            form.add_error('nomCl', 'This name already exist')
            return self.form_invalid(form)
        return super(AjoutClient, self).form_valid(form)


class AjoutCollab(SuccessMessageMixin, CreateView):
    model = Collaborateur
    form_class = AjoutCollabForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('collaborateurs')
    success_message = "Le collaborateur %(collab) aa été créé avec succès."

    def get_context_data(self, **args):
        context = super(CreateView, self).get_context_data(**args)
        context['page_title'] = 'Ajout collaborateur'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            collab=self.object.nomC,
        )

    def form_valid(self, form):
        exist_name = Collaborateur.objects.filter(
                    nomC=form.cleaned_data['nomC'])
        if exist_name:
            form.add_error('nomC', 'This name already exist')
            return self.form_invalid(form)
        return super(AjoutCollab, self).form_valid(form)


class PasserCommande(SuccessMessageMixin, CreateView):
    model = Commande
    form_class = PasserCommandeForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('commandes')
    success_message = "La commande pour le projet %(proj) " + \
                      "aa été passée avec succès."

    def get_context_data(self, **args):
        context = super(CreateView, self).get_context_data(**args)
        context['page_title'] = 'Passer commande'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            proj=self.object.projet.nomP,
        )

    def form_valid(self, form):
        exist = Commande.objects.filter(projet=form.cleaned_data['projet'],
                                        ref=form.cleaned_data['ref'],
                                        etablie=form.cleaned_data['etablie'])
        if exist:
            form.add_error('ref', 'This ref already exist')
            return self.form_invalid(form)

        return super(PasserCommande, self).form_valid(form)


class NouvelleTacheProbable(SuccessMessageMixin, CreateView):
    model = Commande
    form_class = NouvelleTacheProbableForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "La tâche probable pour le projet %(proj) " + \
                      "aa été ajouté avec succès."

    def get_context_data(self, **args):
        context = super(CreateView, self).get_context_data(**args)
        context['page_title'] = 'Ajout tâche probable'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            proj=self.object.projet.nomP,
        )

    def form_valid(self, form):
        exist = Commande.objects.filter(projet=form.cleaned_data['projet'],
                                        ref=form.cleaned_data['ref'])
        if exist:
            form.add_error('ref', 'This ref already exist')
            return self.form_invalid(form)
        return super(NouvelleTacheProbable, self).form_valid(form)


class UpdateProjet(SuccessMessageMixin, UpdateView):
    model = Projet
    form_class = AjoutProjetForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "Le projet %(projet) aa été modifié avec succès."

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification projet'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            projet=self.object.nomP,
        )

    def form_valid(self, form):
        exist = Projet.objects.filter(nomP=form.cleaned_data['nomP'])
        if exist:
            form.add_error('nomP', 'This name already exist')
            return self.form_invalid(form)
        return super(UpdateProjet, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Projet, idProjet=self.kwargs['idProjet'])


class UpdateClient(SuccessMessageMixin, UpdateView):
    model = Client
    form_class = AjoutClientForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('data')
    success_message = "Le client %(client) aa été modifié avec succès."

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification client'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            client=self.object.nomCl,
        )

    def form_valid(self, form):
        exist = Client.objects.filter(nomCl=form.cleaned_data['nomCl'])
        if exist:
            form.add_error('nomCl', 'This name already exist')
            return self.form_invalid(form)
        return super(UpdateClient, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Client, idClient=self.kwargs['idClient'])


class UpdateCollab(SuccessMessageMixin, UpdateView):
    model = Collaborateur
    form_class = AjoutCollabForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('collaborateurs')
    success_message = "Le collaborateur %(collab) aa été modifié avec succès."

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification collaborateur'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            collab=self.object.nomC,
        )

    def form_valid(self, form):
        exist_name = Collaborateur.objects.filter(
                    nomC=form.cleaned_data['nomC'])
        if exist_name:
            form.add_error('nomC', 'This name already exist')
            return self.form_invalid(form)
        return super(UpdateCollab, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Collaborateur,
                                 trigrammeC=self.kwargs['pk'])


class UpdateCommande(SuccessMessageMixin, UpdateView):
    model = Commande
    form_class = UpdateCommandeForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('commandes')
    success_message = "La commande pour le projet %(cmd) aa été modifié " + \
                      "avec succès."

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification commande'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            cmd=self.object.projet.nomP,
        )

    def form_valid(self, form):
        exist = Commande.objects.filter(
            projet=form.cleaned_data['projet'],
            ref=form.cleaned_data['ref'],
            etablie=True)
        if exist:
            form.add_error('ref', 'This ref already exist')
            return self.form_invalid(form)
        if form.cleaned_data['chargesRAF'] > form.cleaned_data['charges']:
            form.add_error('chargesRAF', 'ChargesRAF cannot exceed Charges')
            return self.form_invalid(form)
        return super(UpdateCommande, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande, idCom=self.kwargs['idCom'])


class UpdateTacheProbable(SuccessMessageMixin, UpdateView):
    model = Commande
    form_class = UpdateCommandeForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "La tâche probable pour le projet %(proj) " + \
                      "aa été modifié avec succès."

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification tâche probable'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            proj=self.object.projet.nomP,
        )

    def form_valid(self, form):
        exist = Commande.objects.filter(
            projet=form.cleaned_data['projet'],
            ref=form.cleaned_data['ref'],
            etablie=False)
        exist_cmd = Commande.objects.filter(
            projet=form.cleaned_data['projet'],
            ref=form.cleaned_data['ref'],
            etablie=True)
        if exist or exist_cmd:
            form.add_error('ref', 'This ref already exist')
            return self.form_invalid(form)
        if form.cleaned_data['chargesRAF'] > form.cleaned_data['charges']:
            form.add_error('chargesRAF', 'ChargesRAF cannot exceed Charges')
            return self.form_invalid(form)
        return super(UpdateTacheProbable, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande, idCom=self.kwargs['idCom'])


class DeleteProjet(DeleteView):
    model = Projet
    success_url = reverse_lazy('projets')
    template_name = 'pdc_core_app/del.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Projet, idProjet=self.kwargs['idProjet'])


class DeleteClient(DeleteView):
    model = Client
    success_url = reverse_lazy('data')
    template_name = 'pdc_core_app/del.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Client, idClient=self.kwargs['idClient'])


class DeleteCollab(DeleteView):
    model = Collaborateur
    success_url = reverse_lazy('collaborateurs')
    template_name = 'pdc_core_app/del.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Collaborateur,
                                 trigrammeC=self.kwargs['pk'])


class DeleteTacheProbable(DeleteView):
    model = Commande
    success_url = reverse_lazy('projets')
    template_name = 'pdc_core_app/del.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande,
                                 idCom=self.kwargs['idCom'],
                                 etablie=False)


class DeleteCommande(DeleteView):
    model = Commande
    success_url = reverse_lazy('commandes')
    template_name = 'pdc_core_app/del.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande,
                                 idCom=self.kwargs['idCom'],
                                 etablie=True)


class PassCommandFromTask(UpdateView):
    model = Commande
    form_class = PassCommandFromTaskForm
    template_name = 'pdc_core_app/add.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande, idCom=self.kwargs['idCom'])

    def post(self, request, idCom):
        cmd = self.object = self.get_object()
        cmd.etablie = True
        cmd.save()
        return HttpResponse('Successfully Updated!')


class AffectationCollabProjet(SuccessMessageMixin, CreateView):
    model = RepartitionProjet
    form_class = AffectationCollabProjetForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "Affectation réalisé avec succès."

    def get_context_data(self, **args):
        context = super(CreateView, self).get_context_data(**args)
        context['page_title'] = 'Nouvelle affectation'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            proj=self.object.commande.projet.nomP,
            col=self.object.collaborateur.nomC
        )

    def form_valid(self, form):
        exist = RepartitionProjet.objects.filter(
                    commande=form.cleaned_data['commande'],
                    collaborateur=form.cleaned_data['collaborateur']
                    )
        if exist:
            form.add_error('collaborateur', 'This assignment already exist')
            return self.form_invalid(form)
        affectation = form.save(commit=False)
        date = form.cleaned_data['date']
        prct = form.cleaned_data['pourcentage'].pourcentage
        pourcentage = Pourcentage.objects.get(pourcentage=prct)
        date_month = month.Month(date.year, date.month)
        obj, created = RDate.objects.get_or_create(
                    month=date_month,
                    pourcentage=pourcentage
                    )
        form.save()
        affectation.list_R.add(obj)
        return super(AffectationCollabProjet, self).form_valid(form)
