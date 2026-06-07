from django.contrib import admin
from .models import Profil, Annonce, Message, Matching

# Register your models here.
admin.site.register(Profil)
admin.site.register(Annonce)
admin.site.register(Message)
admin.site.register(Matching)