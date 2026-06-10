from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 

# Importation des tables depuis ton application "profiles"
from profiles.models import Annonce, Profil, Matching

# 1. Action : L'étudiant clique sur "Postuler"
@login_required(login_url='/login/') 
def postuler(request, annonce_id):
    annonce_choisie = Annonce.objects.get(id=annonce_id)
    profil_candidat = request.user.profil 
    
    Matching.objects.create(
        annonce=annonce_choisie,
        candidat=profil_candidat,
        etat='EN_ATTENTE'
    )
    messages.success(request, f"Candidature envoyée pour {annonce_choisie.matiere}.")
    return redirect('annonces')

# 2. Action : Le Mentor Accepte (Avec redirection vers TON chat !)
@login_required(login_url='/login/')
def accepter_candidature(request, matching_id):
    candidature = Matching.objects.get(id=matching_id)
    candidature.etat = 'ACCEPTE'
    candidature.save()
    messages.success(request, f"Vous avez accepté {candidature.candidat.user.username} !")
    
    # LE PONT : On envoie directement le mentor vers ta messagerie !
    return redirect('messaging:boite_reception')

# 3. Action : Le Mentor Refuse
@login_required(login_url='/login/')
def refuser_candidature(request, matching_id):
    candidature = Matching.objects.get(id=matching_id)
    candidature.etat = 'REFUSE'
    candidature.save()
    messages.error(request, f"Candidature refusée.")
    return redirect('mes_annonces')

# 4. L'API /match pour l'algorithme de Sylvain
@login_required(login_url='/login/')
def api_match(request):
    profil_actuel = request.user.profil
    mots_lacunes = [mot.strip() for mot in profil_actuel.lacunes.lower().split(',') if mot.strip()]

    autres_etudiants = Profil.objects.exclude(id=profil_actuel.id)
    suggestions = []

    for potentiel_mentor in autres_etudiants:
        ses_competences = potentiel_mentor.competences.lower()
        score = 0
        matieres_communes = []

        for lacune in mots_lacunes:
            if lacune in ses_competences:
                score += 1
                matieres_communes.append(lacune)

        if score > 0:
            suggestions.append({
                'nom_utilisateur': potentiel_mentor.user.username,
                'filiere': potentiel_mentor.filiere,
                'score_compatibilite': score,
                'matieres_communes': matieres_communes
            })

    suggestions.sort(key=lambda x: x['score_compatibilite'], reverse=True)
    
    return JsonResponse({'matchings_trouves': suggestions})