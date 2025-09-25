from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# 🔹 1. Perfil extendido para el usuario (relación uno a uno)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


