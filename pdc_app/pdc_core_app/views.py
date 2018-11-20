from django.shortcuts import render


def index(request):
    return render(request, 'pdc_core_app/index.html')


def projets(request):
    return render(request, 'pdc_core_app/projets.html')


def collaborateurs(request):
    return render(request, 'pdc_core_app/collaborateurs.html')


def commandes(request):
    return render(request, 'pdc_core_app/commandes.html')


def autres(request):
    return render(request, 'pdc_core_app/autres.html')
