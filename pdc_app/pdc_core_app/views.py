from datetime import datetime as datet, date
from dateutil import relativedelta as rd
from workdays import networkdays
import calendar
from vanilla import DeleteView
import month
import reversion
from reversion.models import Revision, ContentType, Version
from reversion.views import RevisionMixin


from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.apps import apps
from django.contrib.contenttypes.models import ContentType as ModelType
from django.db.models.deletion import ProtectedError

from .models import RepartitionProjet, RepartitionActivite, Commande
from .models import Collaborateur, Responsable_E, Projet, Client, RDate
from .models import Pourcentage, History

from .forms import AjoutClientForm, AjoutCollabForm, PasserCommandeForm
from .forms import AjoutProjetForm, NouvelleTacheProbableForm
from .forms import UpdateCommandeForm, PassCommandFromTaskForm
from .forms import AffectationCollabProjetForm, DateFormSet
from .forms import AffectationCollabActForm, UpdateUserForm


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
            list.extend((rp.idRP, rp.commande.idCom, rp.commande.equipe.nomE,
                         rp.collaborateur.trigrammeC,
                         rp.commande.projet.client.nomCl,
                         rp.commande.projet.nomP, rp.commande.ref,
                         rp.commande.projet.RdP.trigrammeC,
                         rp.commande.projet.RT.trigrammeC,
                         rp.commande.etablie))
        elif type == 'A':
            list.extend((rp.idRA, rp.collaborateur.equipe.nomE,
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


# Calcul charges affectées
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


def assigned_charges_update(request, id):
    v = Version.objects.get_for_object_reference(RepartitionProjet, id)[0]
    cmd_id = v.field_dict['commande_id']
    cmd = Commande.objects.get(idCom=cmd_id)
    charges = assigned_charges(cmd)
    return render(request, 'pdc_core_app/charge_update.html',
                  {"charges": charges})


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
    pourcentagesPP = []
    pourcentagesSP = []
    for rp in repartition:
        listP = []
        listPP = []
        listSP = []
        list_month_repartition = []
        for some in rp.list_R.filter(month__gte=datet.now()):
            list_month_repartition.append(some.month)

        for lm in list_month:
            if lm in list_month_repartition:
                i = list_month_repartition.index(lm)
                pourc_collab = rp.list_R.filter(
                    month__gte=datet.now())[i].pourcentage.pourcentage
                if type == 'P':
                    if rp.commande.etablie is False:
                        listP.append(pourc_collab)
                        prct = (pourc_collab/100)*(rp.commande.odds/100)
                        listPP.append(int(prct*100))
                        listSP.append(0)
                    elif rp.commande.etablie is True:
                        listP.append(pourc_collab)
                        listPP.append(pourc_collab)
                        listSP.append(pourc_collab)
                else:
                    listP.append(pourc_collab)
            else:
                if type == 'P':
                    listP.append(0)
                    listPP.append(0)
                    listSP.append(0)
                else:
                    listP.append(0)
        if type == 'P':
            pourcentages.append(listP)
            pourcentagesPP.append(listPP)
            pourcentagesSP.append(listSP)
        else:
            pourcentages.append(listP)

    if type == 'P':
        return pourcentages, pourcentagesPP, pourcentagesSP
    else:
        return pourcentages


@login_required()
def index(request):
    return render(request, 'pdc_core_app/index.html')


@login_required()
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


@login_required()
def collaborateurs(request):
    page_title = 'Collaborateurs'
    list_month_display = []
    list_month = []
    # Liste finale (all) contenant des listes, chaque liste contenant les
    # informations relative à un collaborateur
    all = []  # cas majorant
    allPP = []  # probable pondéré
    allSP = []  # sans probable
    list_month, list_month_display = get_month(18)
    collaborateurs = Collaborateur.objects.all()
    # Récupération de tous les collaborateurs

    # Pour chaque collaborateur
    for collab in collaborateurs:
        # La list qui contient les informations relative à un seul collab
        # incluant les pourcentages qui sont ajoutés plus bas
        list = []
        listPP = []
        listSP = []
        rde = Responsable_E.objects.filter(equipe=collab.equipe)
        if rde:
            list.extend((collab.equipe.nomE, collab.trigrammeC, rde[0]))
            listPP.extend((collab.equipe.nomE, collab.trigrammeC, rde[0]))
            listSP.extend((collab.equipe.nomE, collab.trigrammeC, rde[0]))
        else:
            list.extend((collab.equipe.nomE, collab.trigrammeC, 'XXX'))
            listPP.extend((collab.equipe.nomE, collab.trigrammeC, 'XXX'))
            listSP.extend((collab.equipe.nomE, collab.trigrammeC, 'XXX'))
    # Dans la liste pourcentagesP on va stocker des listes, chaque liste
    # correspond aux pourcentages par mois d'un projet
        cas_majorant, probable_pondere, sans_probable = get_repartition_wo_inf(
                                                                    'P', collab
                                                                    )
    # De même pour les activité, on fait une liste des pourcentages par
    # activité et on les stocks dans la liste pourcentagesA
        autres = get_repartition_wo_inf('A', collab)
        pourcentagesCM = cas_majorant + autres
        pourcentagesPP = probable_pondere + autres
        pourcentagesSP = sans_probable + autres
    # Maintenant on a donc une liste de liste contenant les pourcentages par
    # projet et par activité. Ainsi on peut faire la somme de tous les éléments
    # de même rang pour avoir la somme des pourcentages par mois.
        for i in range(0, len(list_month)):
            somme = 0
            for p in pourcentagesCM:
                somme += p[i]
            list.append(somme)
        for i in range(0, len(list_month)):
            somme = 0
            for p in pourcentagesPP:
                somme += p[i]
            listPP.append(somme)
        for i in range(0, len(list_month)):
            somme = 0
            for p in pourcentagesSP:
                somme += p[i]
            listSP.append(somme)
        all.append(list)
        allPP.append(listPP)
        allSP.append(listSP)

    return render(request, 'pdc_core_app/collaborateurs.html',
                  {'page_title': page_title,
                   'list_month_display': list_month_display,
                   'all': all, 'allPP': allPP, 'allSP': allSP})


@login_required()
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


@login_required()
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


@login_required()
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


@login_required()
def history(request):
    page_title = "Historique"
    version_list = History.objects.all().order_by('-date')
    return render(request, 'pdc_core_app/history.html',
                  {'page_title': page_title,
                   'version_list': version_list})


def clean_history(request):
    History.objects.all().delete()
    return HttpResponseRedirect(reverse_lazy('history'))


def revision_query(content_model, pk):
    revision = Revision.objects.filter(
        version__content_type=ContentType.objects.get_for_model(content_model)
        ).filter(version__object_id=pk).order_by("-date_created")
    return revision


def revert_history(user, str):
    model_type = ModelType.objects.get(app_label='pdc_core_app',
                                       model='history')
    history = History(
                date=datet.now(),
                user=user,
                model=model_type,
                object_repr=str,
                comment='Undo last action'
                )
    history.save()


@login_required()
def revert_projet(request, model, id):
    Model = apps.get_model('pdc_core_app', model)
    if Model == Commande:
        revision = revision_query(Model, id)
        for rev in revision:
            if rev.get_comment() == "Création commande à" + \
                                    " partir d'une tâche prob.":
                pass
            else:
                rev.revert()
                revert_history(request.user, rev)
                return HttpResponseRedirect(reverse_lazy('projets'))
    else:
        revision = revision_query(Model, id)
        rev = revision[0]
        rev.revert()
        revert_history(request.user, rev)
        return HttpResponseRedirect(reverse_lazy('projets'))


@login_required()
def revert_command(request, model, id):
    Model = apps.get_model('pdc_core_app', model)
    rev = revision_query(Model, id)
    rev[0].revert()
    revert_history(request.user, rev[0])
    return HttpResponseRedirect(reverse_lazy('commandes'))


@login_required()
def revert_collab(request, model, id):
    Model = apps.get_model('pdc_core_app', model)
    rev = revision_query(Model, id)
    rev[0].revert()
    revert_history(request.user, rev[0])
    return HttpResponseRedirect(reverse_lazy('collaborateurs'))


@login_required()
def revert_autres(request, model, id):
    Model = apps.get_model('pdc_core_app', model)
    rev = revision_query(Model, id)
    rev[0].revert()
    revert_history(request.user, rev[0])
    return HttpResponseRedirect(reverse_lazy('autres'))


@login_required()
def revert_data_bis(request, model, id):
    Model = apps.get_model('pdc_core_app', model)
    revision = revision_query(Model, id)
    for rev in revision:
        if rev.get_comment() == "Création commande à partir d'une tâche prob.":
            pass
        else:
            rev.revert()
            revert_history(request.user, rev)
            return HttpResponseRedirect(reverse_lazy('data'))


@login_required()
def revert_data(request, model, id):
    Model = apps.get_model('pdc_core_app', model)
    rev = revision_query(Model, id)
    rev[0].revert()
    revert_history(request.user, rev[0])
    return HttpResponseRedirect(reverse_lazy('data'))


def protected_error(request):
    return render(request, '500.html', status=500)


class AjoutProjet(RevisionMixin, PermissionRequiredMixin, SuccessMessageMixin,
                  CreateView):
    model = Projet
    form_class = AjoutProjetForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "Le projet %(projet) aa été créé avec succès."
    permission_required = ('pdc_core_app.add_projet')

    def post(self, request):
        reversion.set_user(request.user)
        reversion.set_comment("Création projet")
        return super().post(request)

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

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='projet')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Création projet'
                    )
        history.save()
        return super(AjoutProjet, self).form_valid(form)


class AjoutClient(RevisionMixin, PermissionRequiredMixin, SuccessMessageMixin,
                  CreateView):
    model = Client
    form_class = AjoutClientForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('data')
    success_message = "Le client %(client) aa été créé avec succès."
    permission_required = ('pdc_core_app.add_client')

    def post(self, request):
        reversion.set_user(request.user)
        reversion.set_comment("Création client")
        return super().post(request)

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

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='client')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Création client'
                    )
        history.save()
        return super(AjoutClient, self).form_valid(form)


class AjoutCollab(RevisionMixin, PermissionRequiredMixin, SuccessMessageMixin,
                  CreateView):
    model = Collaborateur
    form_class = AjoutCollabForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('collaborateurs')
    success_message = "Le collaborateur %(collab) aa été créé avec succès."
    permission_required = ('pdc_core_app.add_collaborateur')

    def post(self, request):
        reversion.set_user(request.user)
        reversion.set_comment("Création collaborateur")
        return super().post(request)

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

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='collaborateur')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Création collaborateur'
                    )
        history.save()
        return super(AjoutCollab, self).form_valid(form)


class PasserCommande(RevisionMixin, PermissionRequiredMixin,
                     SuccessMessageMixin, CreateView):
    model = Commande
    form_class = PasserCommandeForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "La commande pour le projet %(proj) " + \
                      "aa été passée avec succès."
    permission_required = ('pdc_core_app.add_commande')

    def post(self, request):
        reversion.set_user(request.user)
        reversion.set_comment("Création commande")
        return super().post(request)

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

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='commande')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Création commande'
                    )
        history.save()

        return super(PasserCommande, self).form_valid(form)


class NouvelleTacheProbable(RevisionMixin, PermissionRequiredMixin,
                            SuccessMessageMixin, CreateView):
    model = Commande
    form_class = NouvelleTacheProbableForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "La tâche probable pour le projet %(proj) " + \
                      "aa été ajouté avec succès."
    permission_required = ('pdc_core_app.add_commande')

    def post(self, request):
        reversion.set_user(request.user)
        reversion.set_comment("Création tâche probable")
        return super().post(request)

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

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='commande')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Création tâche probable'
                    )
        history.save()
        return super(NouvelleTacheProbable, self).form_valid(form)


class UpdateProjet(RevisionMixin, PermissionRequiredMixin, SuccessMessageMixin,
                   UpdateView):
    model = Projet
    form_class = AjoutProjetForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "Le projet %(projet) aa été modifié avec succès."
    permission_required = ('pdc_core_app.change_projet')

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Modif. projet")
        return super().post(request)

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification projet'
        context['id'] = self.object.idProjet
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            projet=self.object.nomP,
        )

    def form_valid(self, form):
        exist = Projet.objects.filter(
                            nomP=form.cleaned_data['nomP']
                            ).exclude(
                            idProjet=self.object.idProjet
                            )
        if exist:
            form.add_error('nomP', 'This name already exist')
            return self.form_invalid(form)

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='projet')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='MAJ projet'
                    )
        history.save()
        return super(UpdateProjet, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Projet, idProjet=self.kwargs['idProjet'])


class UpdateClient(RevisionMixin, PermissionRequiredMixin,
                   SuccessMessageMixin, UpdateView):
    model = Client
    form_class = AjoutClientForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('data')
    success_message = "Le client %(client) aa été modifié avec succès."
    permission_required = ('pdc_core_app.change_client')

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Modif. client")
        return super().post(request)

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification client'
        context['id'] = self.object.idClient
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            client=self.object.nomCl,
        )

    def form_valid(self, form):
        exist = Client.objects.filter(
                            nomCl=form.cleaned_data['nomCl']
                            ).exclude(
                            idClient=self.object.idClient
                            )
        if exist:
            form.add_error('nomCl', 'This name already exist')
            return self.form_invalid(form)

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='client')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='MAJ client'
                    )
        history.save()
        return super(UpdateClient, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Client, idClient=self.kwargs['idClient'])


class UpdateCollab(RevisionMixin, PermissionRequiredMixin,
                   SuccessMessageMixin, UpdateView):
    model = Collaborateur
    form_class = AjoutCollabForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('collaborateurs')
    success_message = "Le collaborateur %(collab) aa été modifié avec succès."
    permission_required = ('pdc_core_app.change_collaborateur')

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Modif. collaborateur")
        return super().post(request)

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification collaborateur'
        context['id'] = self.object.trigrammeC
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            collab=self.object.nomC,
        )

    def form_valid(self, form):
        exist_name = Collaborateur.objects.filter(
                    nomC=form.cleaned_data['nomC']).exclude(
                                            trigrammeC=self.object.trigrammeC
                                            )
        if exist_name:
            form.add_error('nomC', 'This name already exist')
            return self.form_invalid(form)

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='collaborateur')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='MAJ collaborateur'
                    )
        history.save()
        return super(UpdateCollab, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Collaborateur,
                                 trigrammeC=self.kwargs['pk'])


class UpdateCommande(RevisionMixin, PermissionRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    model = Commande
    form_class = UpdateCommandeForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('commandes')
    success_message = "La commande pour le projet %(cmd) aa été modifié " + \
                      "avec succès."
    permission_required = ('pdc_core_app.change_commande')

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Modif. commande")
        return super().post(request)

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification commande'
        context['id'] = self.kwargs['idCom']
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
            etablie=True).exclude(idCom=self.object.idCom)
        if exist:
            form.add_error('ref', 'This ref already exist')
            return self.form_invalid(form)
        if form.cleaned_data['chargesRAF'] > form.cleaned_data['charges']:
            form.add_error('chargesRAF', 'ChargesRAF cannot exceed Charges')
            return self.form_invalid(form)

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='commande')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='MAJ commande'
                    )
        history.save()
        return super(UpdateCommande, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande, idCom=self.kwargs['idCom'])


class UpdateTacheProbable(RevisionMixin, PermissionRequiredMixin,
                          SuccessMessageMixin, UpdateView):
    model = Commande
    form_class = UpdateCommandeForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('projets')
    success_message = "La tâche probable pour le projet %(proj) " + \
                      "aa été modifié avec succès."
    permission_required = ('pdc_core_app.change_commande')

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Modif. tâche probable")
        return super().post(request)

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification tâche probable'
        context['id'] = self.object.idCom
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
            etablie=False).exclude(idCom=self.object.idCom)
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

        form_obj = form.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='commande')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='MAJ tâche probable'
                    )
        history.save()
        return super(UpdateTacheProbable, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande, idCom=self.kwargs['idCom'])


class DeleteProjet(RevisionMixin, PermissionRequiredMixin, DeleteView):
    model = Projet
    success_url = reverse_lazy('projets')
    template_name = 'pdc_core_app/del.html'
    permission_required = ('pdc_core_app.delete_projet')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, *args, **kwargs):
        try:
            return self.delete(*args, **kwargs)
        except ProtectedError:
            return HttpResponseRedirect(reverse_lazy('protected_error'))
        else:
            form_obj = self.get_object()

            model_type = ModelType.objects.get(app_label='pdc_core_app',
                                               model='projet')
            history = History(
                        date=datet.now(),
                        user=self.request.user,
                        model=model_type,
                        object_repr=form_obj,
                        comment='Suppression projet'
                        )
            history.save()

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Projet, idProjet=self.kwargs['idProjet'])


class DeleteClient(RevisionMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('data')
    template_name = 'pdc_core_app/del.html'
    permission_required = ('pdc_core_app.delete_client')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, *args, **kwargs):
        form_obj = self.get_object()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='client')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Suppression client'
                    )
        history.save()
        return self.delete(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Client, idClient=self.kwargs['idClient'])


class DeleteCollab(RevisionMixin, PermissionRequiredMixin, DeleteView):
    model = Collaborateur
    success_url = reverse_lazy('collaborateurs')
    template_name = 'pdc_core_app/del.html'
    permission_required = ('pdc_core_app.delete_collaborateur')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, *args, **kwargs):
        form_obj = self.get_object()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='collaborateur')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Suppression collaborateur'
                    )
        history.save()
        return self.delete(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Collaborateur,
                                 trigrammeC=self.kwargs['pk'])


class DeleteTacheProbable(RevisionMixin, PermissionRequiredMixin, DeleteView):
    model = Commande
    success_url = reverse_lazy('projets')
    template_name = 'pdc_core_app/del.html'
    permission_required = ('pdc_core_app.delete_commande')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, *args, **kwargs):
        form_obj = self.get_object()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='commande')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Suppression tâche probable'
                    )
        history.save()
        return self.delete(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande,
                                 idCom=self.kwargs['idCom'],
                                 etablie=False)


class DeleteCommande(RevisionMixin, PermissionRequiredMixin, DeleteView):
    model = Commande
    success_url = reverse_lazy('commandes')
    template_name = 'pdc_core_app/del.html'
    permission_required = ('pdc_core_app.delete_commande')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, *args, **kwargs):
        form_obj = self.get_object()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='commande')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Suppression commande'
                    )
        history.save()
        return self.delete(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande,
                                 idCom=self.kwargs['idCom'],
                                 etablie=True)


class PassCommandFromTask(RevisionMixin, PermissionRequiredMixin, UpdateView):
    model = Commande
    form_class = PassCommandFromTaskForm
    template_name = 'pdc_core_app/add.html'
    permission_required = ('pdc_core_app.change_commande')

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Commande, idCom=self.kwargs['idCom'])

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Création commande à partir d'une tâche prob.")
        cmd = self.object = self.get_object()
        cmd.etablie = True
        cmd.odds = 100
        cmd.save()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='commande')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=cmd,
                    comment='Création commande à partir d\'une tâche probable'
                    )
        history.save()
        return super().post(request)


class AffectationProjetDateSet(RevisionMixin, PermissionRequiredMixin,
                               SuccessMessageMixin, CreateView):
    form_class = AffectationCollabProjetForm
    template_name = 'pdc_core_app/assign.html'
    model = RepartitionProjet
    success_url = reverse_lazy('projets')
    success_message = "Affectation réalisée avec succès."
    permission_required = ('pdc_core_app.add_repartitionprojet')

    def get_context_data(self, **args):
        context = super(CreateView, self).get_context_data(**args)
        context['page_title'] = 'Nouvelle affectation'
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        date_prct_form = DateFormSet()
        return self.render_to_response(self.get_context_data(
                    form=form,
                    date_prct_form=date_prct_form)
                    )

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Création affectation projet")

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        date_prct_form = DateFormSet(self.request.POST)

        if form.is_valid() and date_prct_form.is_valid():
            return self.form_valid(form, date_prct_form)
        else:
            return self.form_invalid(form, date_prct_form)
        return super().post(request)

    def form_valid(self, form, date_prct_form):
        exist = RepartitionProjet.objects.filter(
                    commande=form.cleaned_data['commande'],
                    collaborateur=form.cleaned_data['collaborateur']
                    )
        if exist:
            form.add_error('collaborateur', 'This assignment already exist')
            return self.form_invalid(form, date_prct_form)

        affectation = form.save()

        for date_form in date_prct_form:
            date_form.save(commit=False)
            month = date_form.cleaned_data['month']
            prct = date_form.cleaned_data['pourcentage'].pourcentage
            pourcentage = Pourcentage.objects.get(pourcentage=prct)
            exist = RDate.objects.filter(
                        month=month,
                        pourcentage=pourcentage
                        )
            if exist:
                obj = RDate.objects.get(
                            month=month,
                            pourcentage=pourcentage
                            )
            else:
                obj = date_form.save()
            affectation.list_R.add(obj)

            model_type = ModelType.objects.get(app_label='pdc_core_app',
                                               model='repartitionprojet')
            history = History(
                        date=datet.now(),
                        user=self.request.user,
                        model=model_type,
                        object_repr=affectation,
                        comment='Création affectation projet'
                        )
            history.save()
        return super(AffectationProjetDateSet, self).form_valid(form)

    def form_invalid(self, form, date_prct_form):

        return self.render_to_response(self.get_context_data(
                                    form=form,
                                    date_prct_form=date_prct_form)
                                    )


class UpdateAffectationProjetDateSet(RevisionMixin, PermissionRequiredMixin,
                                     SuccessMessageMixin, UpdateView):
    form_class = AffectationCollabProjetForm
    formset_class = DateFormSet
    template_name = 'pdc_core_app/assign_update.html'
    model = RepartitionProjet
    success_url = reverse_lazy('projets')
    success_message = "Affectation modifiée avec succès."
    permission_required = ('pdc_core_app.change_repartitionprojet')

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification affectation projet'
        context['id'] = self.kwargs['idRP']
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        date_prct_form = DateFormSet(
            initial=[{'month': x.month,
                      'pourcentage': x.pourcentage}
                     for x in self.object.list_R.all()])
        return self.render_to_response(self.get_context_data(
            date_prct_form=date_prct_form,
        ))

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Modif. affectation projet")

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        date_prct_form = DateFormSet(self.request.POST)

        if form.is_valid() and date_prct_form.is_valid():
            return self.form_valid(form, date_prct_form)
        else:
            return self.form_invalid(form, date_prct_form)
        return super().post(request)

    def form_valid(self, form, date_prct_form):
        affectation = form.save()
        self.object = self.get_object()
        RepartitionProjet.objects.get(idRP=self.object.idRP).delete()

        for date_form in date_prct_form:
            date_form.save(commit=False)
            month = date_form.cleaned_data['month']
            prct = date_form.cleaned_data['pourcentage'].pourcentage
            pourcentage = Pourcentage.objects.get(pourcentage=prct)
            exist = RDate.objects.filter(
                        month=month,
                        pourcentage=pourcentage
                        )
            if exist:
                obj = RDate.objects.get(
                            month=month,
                            pourcentage=pourcentage
                            )
            else:
                obj = date_form.save()
            affectation.list_R.add(obj)

            model_type = ModelType.objects.get(app_label='pdc_core_app',
                                               model='repartitionprojet')
            history = History(
                        date=datet.now(),
                        user=self.request.user,
                        model=model_type,
                        object_repr=affectation,
                        comment='MAJ affectation projet'
                        )
            history.save()
        return super(UpdateAffectationProjetDateSet, self).form_valid(form)

    def form_invalid(self, form, date_prct_form):

        return self.render_to_response(self.get_context_data(
                                    form=form,
                                    date_prct_form=date_prct_form)
                                    )

    def get_object(self, *args, **kwargs):
        return get_object_or_404(RepartitionProjet, idRP=self.kwargs['idRP'])


class DeleteAffectation(RevisionMixin, PermissionRequiredMixin, DeleteView):
    model = RepartitionProjet
    success_url = reverse_lazy('projets')
    template_name = 'pdc_core_app/del.html'
    permission_required = ('pdc_core_app.delete_repartitionprojet')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, *args, **kwargs):
        form_obj = self.get_object()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='repartitionprojet')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Suppression affectation projet'
                    )
        history.save()
        return self.delete(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(RepartitionProjet,
                                 idRP=self.kwargs['idRP'],
                                 )


class AffectationAutres(RevisionMixin, PermissionRequiredMixin,
                        SuccessMessageMixin, CreateView):
    form_class = AffectationCollabActForm
    template_name = 'pdc_core_app/assign.html'
    model = RepartitionActivite
    success_url = reverse_lazy('autres')
    success_message = "Affectation réalisée avec succès."
    permission_required = ('pdc_core_app.add_repartitionactivite')

    def get_context_data(self, **args):
        context = super(CreateView, self).get_context_data(**args)
        context['page_title'] = 'Nouvelle activité'
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        date_prct_form = DateFormSet()
        return self.render_to_response(self.get_context_data(
                    form=form,
                    date_prct_form=date_prct_form)
                    )

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Création affectation autres")

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        date_prct_form = DateFormSet(self.request.POST)

        if form.is_valid() and date_prct_form.is_valid():
            return self.form_valid(form, date_prct_form)
        else:
            return self.form_invalid(form, date_prct_form)

    def form_valid(self, form, date_prct_form):
        exist = RepartitionActivite.objects.filter(
                    activite=form.cleaned_data['activite'],
                    collaborateur=form.cleaned_data['collaborateur']
                    )
        if exist:
            form.add_error('collaborateur', 'This assignment already exist')
            return self.form_invalid(form, date_prct_form)

        affectation = form.save()

        for date_form in date_prct_form:
            date_form.save(commit=False)
            month = date_form.cleaned_data['month']
            prct = date_form.cleaned_data['pourcentage'].pourcentage
            pourcentage = Pourcentage.objects.get(pourcentage=prct)
            exist = RDate.objects.filter(
                        month=month,
                        pourcentage=pourcentage
                        )
            if exist:
                obj = RDate.objects.get(
                            month=month,
                            pourcentage=pourcentage
                            )
            else:
                obj = date_form.save()
            affectation.list_R.add(obj)

            model_type = ModelType.objects.get(app_label='pdc_core_app',
                                               model='repartitionactivite')
            history = History(
                        date=datet.now(),
                        user=self.request.user,
                        model=model_type,
                        object_repr=affectation,
                        comment='Création affectation autres'
                        )
            history.save()
        return super(AffectationAutres, self).form_valid(form)

    def form_invalid(self, form, date_prct_form):

        return self.render_to_response(self.get_context_data(
                                    form=form,
                                    date_prct_form=date_prct_form)
                                    )


class UpdateAffectationAutres(RevisionMixin, PermissionRequiredMixin,
                              SuccessMessageMixin, UpdateView):
    form_class = AffectationCollabActForm
    formset_class = DateFormSet
    template_name = 'pdc_core_app/assign_update.html'
    model = RepartitionActivite
    success_url = reverse_lazy('autres')
    success_message = "Affectation modifiée avec succès."
    permission_required = ('pdc_core_app.change_repartitionactivite')

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification affectation activité'
        context['id'] = self.object.idRA
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        date_prct_form = DateFormSet(
            initial=[{'month': x.month,
                      'pourcentage': x.pourcentage}
                     for x in self.object.list_R.all()])
        return self.render_to_response(self.get_context_data(
            date_prct_form=date_prct_form,
        ))

    def post(self, request, *args, **kwargs):
        reversion.set_user(request.user)
        reversion.set_comment("Modif. affectation autres")

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        date_prct_form = DateFormSet(self.request.POST)

        if form.is_valid() and date_prct_form.is_valid():
            return self.form_valid(form, date_prct_form)
        else:
            return self.form_invalid(form, date_prct_form)

    def form_valid(self, form, date_prct_form):
        affectation = form.save()
        self.object = self.get_object()
        RepartitionActivite.objects.get(idRA=self.object.idRA).delete()

        for date_form in date_prct_form:
            date_form.save(commit=False)
            month = date_form.cleaned_data['month']
            prct = date_form.cleaned_data['pourcentage'].pourcentage
            pourcentage = Pourcentage.objects.get(pourcentage=prct)
            exist = RDate.objects.filter(
                        month=month,
                        pourcentage=pourcentage
                        )
            if exist:
                obj = RDate.objects.get(
                            month=month,
                            pourcentage=pourcentage
                            )
            else:
                obj = date_form.save()
            affectation.list_R.add(obj)

            model_type = ModelType.objects.get(app_label='pdc_core_app',
                                               model='repartitionactivite')
            history = History(
                        date=datet.now(),
                        user=self.request.user,
                        model=model_type,
                        object_repr=affectation,
                        comment='MAJ affectation autres'
                        )
            history.save()
        return super(UpdateAffectationAutres, self).form_valid(form)

    def form_invalid(self, form, date_prct_form):

        return self.render_to_response(self.get_context_data(
                                    form=form,
                                    date_prct_form=date_prct_form)
                                    )

    def get_object(self, *args, **kwargs):
        return get_object_or_404(RepartitionActivite, idRA=self.kwargs['idRA'])


class DeleteAffectationAutres(RevisionMixin, PermissionRequiredMixin,
                              DeleteView):
    model = RepartitionProjet
    success_url = reverse_lazy('projets')
    template_name = 'pdc_core_app/del.html'
    permission_required = ('pdc_core_app.delete_repartitionactivite')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, *args, **kwargs):
        form_obj = self.get_object()

        model_type = ModelType.objects.get(app_label='pdc_core_app',
                                           model='repartitionactivite')
        history = History(
                    date=datet.now(),
                    user=self.request.user,
                    model=model_type,
                    object_repr=form_obj,
                    comment='Suppression affectation autres'
                    )
        history.save()
        return self.delete(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(RepartitionActivite,
                                 idRA=self.kwargs['idRA'],
                                 )


class UpdateUser(UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'pdc_core_app/add.html'
    success_url = reverse_lazy('login')
    success_message = "Utilisateur modifiée avec succès."

    def get_context_data(self, **args):
        context = super(UpdateView, self).get_context_data(**args)
        context['page_title'] = 'Modification utilisateur'
        return context

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, id=self.kwargs['id'])
