from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

# clase base de timestamp

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # cuando se crea
    updated_at = models.DateTimeField(auto_now=True) # cuando se actualiza

    class Meta:
        abstract = True


# 🔹 1. Perfil extendido para el usuario (relación uno a uno)
class UserProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], blank=True)
    headline = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True)
    role = models.CharField(
        max_length=100,
        choices=[
            ('user', 'User'),
            ('premium', 'Premium'),
            ('admin', 'Admin'),
            ('teacher', 'Teacher'),
            ('headhunter', 'Headhunter'),
            ('professional', 'Professional')
        ],
        default='user'
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


 # Validaciones
    # ----------------------------
    def clean(self):
        # Validar que la fecha de nacimiento no sea futura
        if self.birthdate and self.birthdate > timezone.now().date():
            raise ValidationError({"birthdate": "La fecha de nacimiento no puede ser futura."})

        # Validar longitud mínima de teléfono (opcional)
        if self.phone and len(self.phone) < 7:
            raise ValidationError({"phone": "El número de teléfono es demasiado corto."})