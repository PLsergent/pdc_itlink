from django.shortcuts import render
from datetime import datetime as datet
from dateutil import relativedelta as rd
from .models import RepartitionProjet, RepartitionActivite, Commande
import month


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

    for rp in repartitions:
        list = []
        if type == 'P':
            list.extend((rp.commande.equipe.nomE, rp.collaborateur.trigrammeC,
                         rp.commande.projet.client.nomCl,
                         rp.commande.projet.nomP,
                         rp.commande.projet.RdP.trigrammeC,
                         rp.commande.projet.RT.trigrammeC,
                         rp.commande.etablie))
        elif type == 'A':
            list.extend((rp.collaborateur.trigrammeC,
                         rp.collaborateur.equipe.nomE,
                         rp.activite))
        else:
            return None

        list_month_repartition = []
        for some in rp.list_R.filter(month__gte=datet.now()):
            list_month_repartition.append(some.month)

        for lm in list_month:
            if lm in list_month_repartition:
                i = list_month_repartition.index(lm)
                pourc_collab = rp.list_R.filter(
                    month__gte=datet.now())[i].pourcentage
                list.append(pourc_collab)
            else:
                list.append(0)
        all.append(list)
    return list_month, list_month_display, all


def index(request):
    return render(request, 'pdc_core_app/index.html')


def projets(request):
    page_title = 'Projets'
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
    return render(request, 'pdc_core_app/collaborateurs.html',
                  {'page_title': page_title})


def commandes(request):
    page_title = 'Commandes'
    all = []
    commandes = Commande.objects.all()

    for cmd in commandes:
        list = []
        list.extend((cmd.equipe.nomE, cmd.date_commande, cmd.projet.nomP,
                     cmd.projet.RdP.trigrammeC, cmd.charges, cmd.ref,
                     cmd.etablie, cmd.commentaire))
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
