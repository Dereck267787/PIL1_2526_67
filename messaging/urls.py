from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # 1. La route pour afficher la page de la messagerie (le design d'Abdel)
    path('', views.boite_reception, name='boite_reception'),
    
    # 2. La route invisible (API) pour que le JavaScript envoie/récupère les messages
    path('api/<int:correspondant_id>/', views.api_messages, name='api_messages'),
]