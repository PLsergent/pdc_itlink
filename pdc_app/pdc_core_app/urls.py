from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projets/', views.projets, name='projets'),
    path('collaborateurs/', views.collaborateurs, name='collaborateurs'),
    path('commandes/', views.commandes, name='commandes'),
    path('autres/', views.autres, name='autres'),
]
