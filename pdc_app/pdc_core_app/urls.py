from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projets/', views.projets, name='projets'),
    path('projets/add/', views.AjoutProjet.as_view(),
         name='AjoutProjet'),
    path('clients/add/', views.AjoutClient.as_view(),
         name='AjoutClient'),
    path('collaborateurs/', views.collaborateurs, name='collaborateurs'),
    path('commandes/', views.commandes, name='commandes'),
    path('autres/', views.autres, name='autres'),
    path('data/', views.data, name='data')
]
