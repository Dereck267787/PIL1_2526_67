from django.db import models
from django.contrib.auth.models import User # Importe la table utilisateur de base de Django

# 1. TABLE PROFIL : Pour stocker les infos de l'étudiant
class Profil(models.Model):
    # Les choix possibles pour le niveau d'étude
    NIVEAUX = [
        ('L1', 'Licence 1'), ('L2', 'Licence 2'), ('L3', 'Licence 3'),
        ('M1', 'Master 1'), ('M2', 'Master 2')
    ]
    
    # On relie ce profil au compte utilisateur classique (celui qui a le mot de passe)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    photo = models.ImageField(upload_to='avatars/', null=True, blank=True)
    filiere = models.CharField(max_length=100, help_text="Ex: Génie Logiciel, IA...", blank=True, null=True)
    niveau = models.CharField(max_length=2, choices=NIVEAUX, blank=True, null=True)

    # AJOUT DE blank=True, null=True SUR CES DEUX LIGNES :
    competences = models.TextField(help_text="Matières maîtrisées (séparées par des virgules)", blank=True, null=True)
    lacunes = models.TextField(help_text="Matières où l'étudiant a besoin d'aide", blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

# 2. TABLE ANNONCE : Les offres et demandes de mentorat
class Annonce(models.Model):
    TYPES = [('OFFRE', 'Offre de mentorat'), ('DEMANDE', 'Demande de mentorat')]
    FORMATS = [('EN_LIGNE', 'En ligne'), ('PRESENTIEL', 'Présentiel')]

    auteur = models.ForeignKey(Profil, on_delete=models.CASCADE)
    type_annonce = models.CharField(max_length=10, choices=TYPES)
    matiere = models.CharField(max_length=100)
    format_cours = models.CharField(max_length=15, choices=FORMATS)
    disponibilites = models.CharField(max_length=255, help_text="Ex: Samedi matin, Jeudi soir")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_annonce} - {self.matiere} par {self.auteur.user.username}"

# 3. TABLE MESSAGE : Pour le système de messagerie
class Message(models.Model):
    expediteur = models.ForeignKey(User, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(User, related_name='messages_recus', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.expediteur} à {self.destinataire}"

# 4. TABLE MATCHING : Pour gérer les mises en relation (candidatures)
class Matching(models.Model):
    ETATS = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTE', 'Accepté'),
        ('REFUSE', 'Refusé'),
        ('TERMINE', 'Terminé')
    ]

    # On relie le matching à l'annonce concernée et au profil qui postule
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='candidatures')
    candidat = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='mes_candidatures')
    
    # L'état actuel de la demande (par défaut, c'est "En attente")
    etat = models.CharField(max_length=20, choices=ETATS, default='EN_ATTENTE')
    date_demande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidat.user.username} -> {self.annonce.matiere} ({self.get_etat_display()})"