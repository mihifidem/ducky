from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.text import slugify
import os
from django.conf import settings
from django.core.exceptions import ValidationError

# librerias necesarias para el qr
# from django.core.files.base import ContentFile
# import qrcode
# from io import BytesIO
# 🔹 1. Experiencia laboral del usuario (relación muchos a uno)
class UserJobExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.position} at {self.company}"

# 🔹 2. Habilidades fuertes y relación con usuario (N-M)
class HardSkill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserHardSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(HardSkill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.skill.name}"
        
# 🔹 3. Habilidades blandas y relación con usuario (N-M)
class SoftSkill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserSoftSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(SoftSkill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.skill.name}"


# 🔹 4. Idiomas y nivel, con relación usuario-idioma (N-M)
class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserLanguage(models.Model):
    LEVEL_CHOICES = [
        ("A1", "A1 – Beginner"),
        ("A2", "A2 – Elementary"),
        ("B1", "B1 – Intermediate"),
        ("B2", "B2 – Upper‑intermediate"),
        ("C1", "C1 – Advanced"),
        ("C2", "C2 – Proficient"),
        ("N", "Native")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, verbose_name="Nivel")

    class Meta:
        unique_together = ("user", "language")  # Evita idiomas duplicados por usuario

    def __str__(self):
        return f"{self.language} ({self.level})"


# 🔹 5. Pasatiempos (hobbies) y relación usuario-hobby (N-M)
class Hobby(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserHobby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    def __str__(self):
        return f"{self.hobby.name}"


# 🔹 6. Educación del usuario (1-N)
class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.institution}"


# 🔹 Modelo para perfiles de CV (con personalización y selección de secciones)
class CVProfile(models.Model):
    primary_color = models.CharField(max_length=20, default="#000000")
    font_family = models.CharField(max_length=50, default="sans-serif")
    header_image = models.ImageField(upload_to='cv_headers/', blank=True, null=True)

    SKIN_CHOICES = [
        ('default', 'Clásico'),
        ('modern', 'Moderno'),
        ('minimal', 'Minimalista'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cv_profiles')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    skin = models.CharField(max_length=50, choices=SKIN_CHOICES, default='default')
    # qr = models.ImageField(upload_to='cv_qr/', blank=True, null=True)
    
    # Relaciones M2M para seleccionar qué datos incluir en el CV
    selected_experiences = models.ManyToManyField(UserJobExperience, blank=True)
    selected_educations = models.ManyToManyField(UserEducation, blank=True)
    selected_softskills = models.ManyToManyField(UserSoftSkill, blank=True)
    selected_hardskills = models.ManyToManyField(UserHardSkill, blank=True)
    selected_languages = models.ManyToManyField(UserLanguage, blank=True)
    selected_hobbies = models.ManyToManyField(UserHobby, blank=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def save(self, *args, **kwargs):
        # Crear slug único basado en username y título del CV
        if not self.slug:
            base_slug = slugify(f"{self.user.username}-{self.title}")
            count = 1
            unique_slug = base_slug
            while CVProfile.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{count}"
                count += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


