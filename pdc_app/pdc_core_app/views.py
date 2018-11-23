from django.shortcuts import render
from datetime import datetime as datet
from dateutil import relativedelta as rd
from .models import RepartitionProjet, RepartitionActivite, Commande
from .models import Collaborateur, Responsable_E
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
    # Information : colonnes de gauche
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
    list_month_display = []
    list_month = []
# Liste (all) finale contenant des listes, chaque liste contenant les
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
        list.extend((collab.equipe.nomE, collab.trigrammeC, rde[0]))
        repartitionP = RepartitionProjet.objects.filter(collaborateur=collab)
        repartitionA = RepartitionActivite.objects.filter(collaborateur=collab)
        pourcentages = []
    # Dans la liste pourcentages on va stocker des listes, chaque liste
    # correspond aux pourcentages par mois d'un projet
        for rp in repartitionP:
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
    # De même pour les activité, on fait une liste des pourcentages par
    # activité et on les stocks dans la liste pourcentage
        for ra in repartitionA:
            listP = []
            list_month_repartition = []
            for some in ra.list_R.filter(month__gte=datet.now()):
                list_month_repartition.append(some.month)

            for lm in list_month:
                if lm in list_month_repartition:
                    i = list_month_repartition.index(lm)
                    pourc_collab = ra.list_R.filter(
                        month__gte=datet.now())[i].pourcentage.pourcentage
                    listP.append(pourc_collab)
                else:
                    listP.append(0)
            pourcentages.append(listP)
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
        list.extend((cmd.equipe.nomE, cmd.date_commande,
                     cmd.projet.client.nomCl, cmd.projet.nomP,
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
