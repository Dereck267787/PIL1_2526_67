from django.db import models
from django.contrib.auth.models import User

class CompteUtilisateur(models.Model):
    CHOIX_ROLE = [
        ('mentor', 'Mentor'),
        ('mentore', 'Mentoré'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='compte')
    role = models.CharField(max_length=10, choices=CHOIX_ROLE)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
# Create your models here.
