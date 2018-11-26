from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projets/', views.projets, name='projets'),
    path('projets/add/', views.AjoutProjet.as_view(),
         name='AjoutProjet'),
    path('collaborateurs/', views.collaborateurs, name='collaborateurs'),
    path('commandes/', views.commandes, name='commandes'),
    path('autres/', views.autres, name='autres'),
]
