from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projets/', views.projets, name='projets'),
    path('projets/add/', views.AjoutProjet.as_view(),
         name='AjoutProjet'),
    path('projets/update/<int:idProjet>/', views.UpdateProjet.as_view(),
         name='UpdateProjet'),
    path('projets/delete/<int:idProjet>/', views.DeleteProjet.as_view(),
         name='DeleteProjet'),
    path('projets/tache_probable_add/', views.NouvelleTacheProbable.as_view(),
         name='NouvelleTacheProbable'),
    path('projets/tache_probable_update/<int:idCom>',
         views.ModifTacheProbable.as_view(),
         name='ModifTacheProbable'),

    path('clients/add/', views.AjoutClient.as_view(), name='AjoutClient'),
    path('clients/update/<int:idClient>/', views.UpdateClient.as_view(),
         name='UpdateClient'),

    path('collaborateurs/', views.collaborateurs, name='collaborateurs'),
    path('collaborateurs/add/', views.AjoutCollab.as_view(),
         name='AjoutCollab'),
    path('collaborateurs/update/<str:pk>', views.UpdateCollab.as_view(),
         name='UpdateCollab'),

    path('commandes/', views.commandes, name='commandes'),
    path('commandes/add/', views.PasserCommande.as_view(),
         name='PasserCommande'),

    path('autres/', views.autres, name='autres'),
    path('data/', views.data, name='data')
]
