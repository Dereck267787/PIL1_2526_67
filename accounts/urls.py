from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # --- LA RACINE DU SITE (PAGE D'ACCUEIL) ---
    path('', views.accueil_view, name='accueil'),
    
    # --- LE NOUVEAU TABLEAU DE BORD ---
    path('dashboard/', views.dashboard_view, name='dashboard'), # <-- NOUVEAU ICI !
    
    # --- AUTHENTIFICATION ---
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # --- LES AUTRES PAGES ---
    path('profil/', views.profil_view, name='profil'),
    path('matching/', views.matching_view, name='matching'),
    path('offres/', views.offres_view, name='offres'),
    path('dispo/', views.dispo_view, name='dispo'),
    path('competences/', views.competences_view, name='competences'),
    path('notifications/', views.notifications_view, name='notifications'),
]