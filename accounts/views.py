from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CompteUtilisateur

# 1. Vue pour l'Inscription (Register)
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role') # 'mentor' ou 'mentore'

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, 'accounts/register.html')

        # Créer l'utilisateur de base Django
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Créer le profil associé avec le rôle choisi
        CompteUtilisateur.objects.create(user=user, role=role)
        
        # Connecter automatiquement l'utilisateur et rediriger
        login(request, user)
        return redirect('profile') # Redirige vers la page profil

    return render(request, 'accounts/register.html')

# 2. Vue pour la Connexion (Login)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'accounts/login.html')

# 3. Vue pour la Déconnexion (Logout)
def logout_view(request):
    logout(request)
    return redirect('login')
# Create your views here.
