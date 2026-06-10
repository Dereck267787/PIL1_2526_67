


import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q # L'outil pour faire des recherches "OU"

# On importe Message ET Matching depuis tes tables de l'application profiles
from profiles.models import Message, Matching 

# --- ÉTAPE 1 : La page qui affiche la liste de contacts et la messagerie ---
@login_required(login_url='/login/')
def boite_reception(request):
    profil_actuel = request.user.profil
    
    # On cherche tous les matchings ACCEPTÉS qui te concernent
    matchings_valides = Matching.objects.filter(
        Q(candidat=profil_actuel) | Q(annonce__auteur=profil_actuel),
        etat='ACCEPTE'
    )
    
    # On crée la liste de tes contacts
    liste_contacts = []
    for match in matchings_valides:
        if match.candidat == profil_actuel:
            liste_contacts.append(match.annonce.auteur.user)
        else:
            liste_contacts.append(match.candidat.user)
            
    # On supprime les doublons
    liste_contacts = list(set(liste_contacts))

    # ICI : On pointe bien vers le fichier d'Abdel (index mess.html) !
    return render(request, 'messaging/index_mess.html', {'contacts': liste_contacts})


# --- L'API : Le moteur qui gère l'envoi et la réception en arrière-plan ---
@csrf_exempt 
@login_required(login_url='/login/')
def api_messages(request, correspondant_id):
    utilisateur_actuel = request.user
    
    # SI LE JAVASCRIPT DEMANDE À LIRE LES MESSAGES
    if request.method == 'GET':
        messages = Message.objects.filter(
            expediteur__in=[utilisateur_actuel.id, correspondant_id],
            destinataire__in=[utilisateur_actuel.id, correspondant_id]
        ).order_by('date_envoi')
        
        donnees = []
        for msg in messages:
            donnees.append({
                'expediteur_id': msg.expediteur.id,
                'contenu': msg.contenu,
                'date': msg.date_envoi.strftime("%H:%M") 
            })
            
        return JsonResponse({'messages': donnees})

    # SI LE JAVASCRIPT ENVOIE UN NOUVEAU MESSAGE
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            texte_message = body.get('contenu')
            
            destinataire_obj = User.objects.get(id=correspondant_id)
            
            Message.objects.create(
                expediteur=utilisateur_actuel,
                destinataire=destinataire_obj,
                contenu=texte_message
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)