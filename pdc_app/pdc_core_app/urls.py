from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),

    path('projets/', views.projets, name='projets'),
    path('projets/add/', views.AjoutProjet.as_view(),
         name='AjoutProjet'),
    path('projets/update/<int:idProjet>', views.UpdateProjet.as_view(),
         name='UpdateProjet'),
    path('projets/delete/<int:idProjet>', views.DeleteProjet.as_view(),
         name='DeleteProjet'),
    path('projets/tache_probable_add/', views.NouvelleTacheProbable.as_view(),
         name='NouvelleTacheProbable'),
    path('projets/tache_probable_update/<int:idCom>',
         views.UpdateTacheProbable.as_view(),
         name='UpdateTacheProbable'),
    path('projets/tache_probable_delete/<int:idCom>',
         views.DeleteTacheProbable.as_view(),
         name='DeleteTacheProbable'),

    path('clients/add/', views.AjoutClient.as_view(), name='AjoutClient'),
    path('clients/update/<int:idClient>', views.UpdateClient.as_view(),
         name='UpdateClient'),
    path('clients/delete/<int:idClient>', views.DeleteClient.as_view(),
         name='DeleteClient'),

    path('collaborateurs/', views.collaborateurs, name='collaborateurs'),
    path('collaborateurs/add/', views.AjoutCollab.as_view(),
         name='AjoutCollab'),
    path('collaborateurs/update/<str:pk>', views.UpdateCollab.as_view(),
         name='UpdateCollab'),
    path('collaborateurs/delete/<str:pk>', views.DeleteCollab.as_view(),
         name='DeleteCollab'),
    path('collaborateurs/assign/', views.AffectationProjetDateSet.as_view(),
         name='AffectationProjetDateSet'),
    path('collaborateurs/assign/update/<int:idRP>',
         views.UpdateAffectationProjetDateSet.as_view(),
         name='UpdateAffectationProjetDateSet'),
    path('collaborateurs/assign/delete/<int:idRP>',
         views.DeleteAffectation.as_view(),
         name='DeleteAffectation'),

    path('commandes/', views.commandes, name='commandes'),
    path('commandes/add/', views.PasserCommande.as_view(),
         name='PasserCommande'),
    path('commandes/update/<int:idCom>', views.UpdateCommande.as_view(),
         name='UpdateCommande'),
    path('commandes/fromtask/<int:idCom>', views.PassCommandFromTask.as_view(),
         name='PassCommandFromTask'),
    path('commandes/delete/<int:idCom>', views.DeleteCommande.as_view(),
         name='DeleteCommande'),

    path('autres/', views.autres, name='autres'),
    path('autres/assign', views.AffectationAutres.as_view(),
         name='AffectationAutres'),
    path('autres/assign/update/<int:idRA>',
         views.UpdateAffectationAutres.as_view(),
         name='UpdateAffectationAutres'),
    path('autres/assign/delete/<int:idRA>',
         views.DeleteAffectationAutres.as_view(),
         name='DeleteAffectationAutres'),
    path('data/', views.data, name='data')
]
