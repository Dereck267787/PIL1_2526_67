from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    # Route pour postuler à une annonce
    path('postuler/<int:annonce_id>/', views.postuler, name='postuler'),
    
    # Routes pour le mentor (accepter ou refuser)
    path('accepter/<int:matching_id>/', views.accepter_candidature, name='accepter_candidature'),
    path('refuser/<int:matching_id>/', views.refuser_candidature, name='refuser_candidature'),
    
    # Route pour l'algorithme de matching
    path('api/match/', views.api_match, name='api_match'),
]