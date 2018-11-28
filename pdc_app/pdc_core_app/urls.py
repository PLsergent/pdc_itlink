from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projets/', views.projets, name='projets'),
    path('projets/add/', views.AjoutProjet.as_view(),
         name='AjoutProjet'),
    path('projets/tache_probable_add/', views.NouvelleTacheProbable.as_view(),
         name='NouvelleTacheProbable'),
    path('clients/add/', views.AjoutClient.as_view(),
         name='AjoutClient'),
    path('collaborateurs/', views.collaborateurs, name='collaborateurs'),
    path('collaborateurs/add/', views.AjoutCollab.as_view(),
         name='AjoutCollab'),
    path('commandes/', views.commandes, name='commandes'),
    path('commandes/add/', views.PasserCommande.as_view(),
         name='PasserCommande'),
    path('autres/', views.autres, name='autres'),
    path('data/', views.data, name='data')
]
