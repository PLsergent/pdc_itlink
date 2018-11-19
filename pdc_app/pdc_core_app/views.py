from django.shortcuts import render


def index(request):
    return render(request, 'pdc_core_app/index.html')
