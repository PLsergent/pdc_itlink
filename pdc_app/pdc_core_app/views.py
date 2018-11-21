from django.shortcuts import render
from datetime import datetime as datet
from dateutil import relativedelta as rd
from .models import RepartitionProjet


def index(request):
    return render(request, 'pdc_core_app/index.html')


def projets(request):
    page_title = 'Projets'
    list_month_display = []
    for i in range(0, 12):
        date_month_after = datet.now() + rd.relativedelta(months=i)
        list_month_display.append((date_month_after.month, date_month_after.year))
    repartitions = RepartitionProjet.objects.all()
    return render(request, 'pdc_core_app/projets.html',
                  {'page_title': page_title,
                   'list_month_display': list_month_display,
                   'repartitions': repartitions})


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
