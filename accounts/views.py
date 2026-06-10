from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# On importe les tables de ta base de données
from .models import CompteUtilisateur
from profiles.models import Profil, Matching, Message, Annonce

# ==========================================
# 1. AUTHENTIFICATION (Inscription, Connexion, Déconnexion)
# ==========================================

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password') 
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'accounts/index_ins.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, 'accounts/index_ins.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        CompteUtilisateur.objects.create(user=user, role=role)
        Profil.objects.create(user=user)
        
        login(request, user)
        return redirect('accounts:dashboard') 

    return render(request, 'accounts/index_ins.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard') 
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'accounts/index.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:accueil')


# ==========================================
# 2. PAGES DU SITE
# ==========================================

def accueil_view(request):
    return render(request, 'accounts/index.html') 


@login_required(login_url='/login/')
def dashboard_view(request):
    profil_actuel = request.user.profil
    nb_matches_reels = Matching.objects.filter(
        Q(candidat=profil_actuel) | Q(annonce__auteur=profil_actuel),
        etat='ACCEPTE'
    ).count()

    nb_messages_non_lus = Message.objects.filter(destinataire=request.user).count()

    context = {
        'total_matches': nb_matches_reels,
        'total_messages': nb_messages_non_lus,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='/login/')
def profil_view(request):
    return render(request, 'accounts/index_profil.html')


@login_required(login_url='/login/')
def matching_view(request):
    profil_actuel = request.user.profil
    
    # Récupérer les vrais matches depuis MySQL
    matches_actifs = Matching.objects.filter(
        Q(candidat=profil_actuel) | Q(annonce__auteur=profil_actuel),
        etat='ACCEPTE'
    )
    matches_en_attente = Matching.objects.filter(
        Q(candidat=profil_actuel) | Q(annonce__auteur=profil_actuel),
        etat='EN_ATTENTE'
    )
    
    # Simuler des suggestions avec les autres profils inscrits à l'IFRI
    suggestions = Profil.objects.exclude(id=profil_actuel.id)[:3]

    context = {
        'matches_actifs': matches_actifs,
        'matches_en_attente': matches_en_attente,
        'suggestions': suggestions
    }
    return render(request, 'accounts/index_matc.html', context)


@login_required(login_url='/login/')
def competences_view(request):
    profil = request.user.profil
    
    # Si l'étudiant valide le formulaire d'enregistrement
    if request.method == 'POST':
        profil.competences = request.POST.get('competences', '')
        profil.lacunes = request.POST.get('lacunes', '')
        profil.save()
        messages.success(request, "Compétences enregistrées avec succès !")
        return redirect('accounts:competences')

    # Suggestions : les profils qui ont en compétences ce que j'ai en lacunes
    suggestions_compatibles = Profil.objects.exclude(user=request.user)[:2]

    return render(request, 'accounts/index_comp.html', {
        'profil': profil,
        'suggestions': suggestions_compatibles
    })


@login_required(login_url='/login/')
def profil_view(request):
    profil = request.user.profil
    
    if request.method == 'POST':
        # 1. On met à jour les informations classiques (User)
        request.user.first_name = request.POST.get('prenom', request.user.first_name)
        request.user.last_name = request.POST.get('nom', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        # 2. On met à jour les informations IFRI (Profil)
        profil.filiere = request.POST.get('filiere', profil.filiere)
        profil.niveau = request.POST.get('niveau', profil.niveau)
        
        # 3. La magie de l'image : on la récupère si elle a été envoyée
        if 'photo' in request.FILES:
            profil.photo = request.FILES['photo']
            
        profil.save()
        messages.success(request, "Ton profil a été mis à jour avec succès !")
        return redirect('accounts:profil')
        
    return render(request, 'accounts/index_profil.html', {'profil': profil})


@login_required(login_url='/login/')
def offres_view(request):
    profil = request.user.profil
    
    if request.method == 'POST':
        # CAS 1 : L'étudiant crée une NOUVELLE OFFRE/DEMANDE
        if 'creer_annonce' in request.POST:
            Annonce.objects.create(
                auteur=profil,
                type_annonce=request.POST.get('type'),
                matiere=request.POST.get('matiere'),
                format_cours=request.POST.get('format'),
                disponibilites=request.POST.get('dispo')
            )
            return redirect('accounts:offres')
            
        # CAS 2 : L'étudiant clique sur RÉPONDRE (Création du Match !)
        elif 'repondre_annonce' in request.POST:
            annonce_id = request.POST.get('annonce_id')
            annonce_cible = Annonce.objects.get(id=annonce_id)
            
            # On vérifie qu'il ne postule pas à sa propre annonce
            if annonce_cible.auteur != profil:
                Matching.objects.get_or_create(
                    annonce=annonce_cible,
                    candidat=profil
                    # L'état est "EN_ATTENTE" par défaut grâce à ton modèle MySQL !
                )
            return redirect('accounts:offres')

    # On récupère toutes les annonces de la base de données (les plus récentes en premier)
    toutes_les_annonces = Annonce.objects.all().order_by('-date_creation')
    
    return render(request, 'accounts/index_offre.html', {'annonces': toutes_les_annonces})


@login_required(login_url='/login/')
def notifications_view(request):
    profil = request.user.profil
    
    # On cherche les gens qui ont répondu à MES annonces et qui sont en attente
    demandes_recues = Matching.objects.filter(annonce__auteur=profil, etat='EN_ATTENTE')
    
    # Si je clique sur "Accepter" ou "Refuser"
    if request.method == 'POST':
        match_id = request.POST.get('match_id')
        action = request.POST.get('action')
        
        if match_id and action:
            match_candidature = Matching.objects.get(id=match_id)
            
            if action == 'accepter':
                match_candidature.etat = 'ACCEPTE' # C'est CA qui débloque le chat !
            elif action == 'refuser':
                match_candidature.etat = 'REFUSE'
                
            match_candidature.save()
            return redirect('accounts:notifications')

    return render(request, 'accounts/index_notif.html', {'demandes_recues': demandes_recues})


@login_required(login_url='/login/')
def dispo_view(request):
    return render(request, 'accounts/index_dispo.html')