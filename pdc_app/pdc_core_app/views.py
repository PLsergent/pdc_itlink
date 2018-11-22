from django.shortcuts import render
from datetime import datetime as datet
from dateutil import relativedelta as rd
from .models import RepartitionProjet
import month


def index(request):
    return render(request, 'pdc_core_app/index.html')


def projets(request):
    page_title = 'Projets'
    list_month_display = []
    list_month = []
    all = []
    for i in range(0, 13):
        date_month_after = datet.now() + rd.relativedelta(months=i)
        list_month_display.append((date_month_after.month, date_month_after.year))
        list_month.append(month.Month(date_month_after.year, date_month_after.month))
    repartitions = RepartitionProjet.objects.all()
    for rp in repartitions:
        list = []
        list.extend((rp.commande.equipe.nomE, rp.collaborateur.trigrammeC,
                     rp.commande.projet.client.nomCl, rp.commande.projet.nomP,
                     rp.commande.projet.RdP.trigrammeC,
                     rp.commande.projet.RT.trigrammeC, rp.commande.etablie))
        list_month_repartition = []
        for some in rp.list_R.filter(month__gte=datet.now()):
            list_month_repartition.append(some.month)

        for lm in list_month:
            if lm in list_month_repartition:
                i = list_month_repartition.index(lm)
                pourc = rp.list_R.filter(month__gte=datet.now())[i].pourcentage
                list.append(pourc)
            else:
                list.append(0)
        all.append(list)
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
    return render(request, 'pdc_core_app/commandes.html',
                  {'page_title': page_title})


def autres(request):
    page_title = 'Autres'
    return render(request, 'pdc_core_app/autres.html',
                  {'page_title': page_title})
