from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulaire, name='formulaire'),
    path('liste/', views.liste, name='liste'),
    path('pdf/', views.generate_pdf, name='generate_pdf'),
]