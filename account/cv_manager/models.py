from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.text import slugify
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


# librerias necesarias para el qr

# import qrcode

# from io import BytesIO


# clase base de timestamp
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # cuando se crea
    updated_at = models.DateTimeField(auto_now=True) # cuando se actualiza

    class Meta:
        abstract = True


# 🔹 1. Experiencia laboral del usuario (relación muchos a uno)
class UserJobExperience(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]
        indexes = [models.Index(fields=["user", "start_date"])]

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("La fecha de fin no puede ser menor que la de inicio")

    def __str__(self):
        return f"{self.position} at {self.company}"
    

# 🔹 2. Habilidades fuertes y relación con usuario (N-M)
class HardSkill(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserHardSkill(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey(HardSkill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.skill.name}"
        
# 🔹 3. Habilidades blandas y relación con usuario (N-M)
class SoftSkill(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserSoftSkill(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey(SoftSkill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.skill.name}"


# 🔹 4. Idiomas y nivel, con relación usuario-idioma (N-M)
class Language(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserLanguage(TimeStampedModel):
    LEVEL_CHOICES = [
        ("A1", "A1 – Beginner"),
        ("A2", "A2 – Elementary"),
        ("B1", "B1 – Intermediate"),
        ("B2", "B2 – Upper‑intermediate"),
        ("C1", "C1 – Advanced"),
        ("C2", "C2 – Proficient"),
        ("N", "Native")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, verbose_name="Nivel")

    class Meta:
        unique_together = ("user", "language")  # Evita idiomas duplicados por usuario

    def __str__(self):
        return f"{self.language} ({self.level})"


# 🔹 5. Pasatiempos (hobbies) y relación usuario-hobby (N-M)
class Hobby(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserHobby(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    class Meta:
        unique_together = ('user', 'hobby', 'description')

    def __str__(self):
        return f"{self.hobby.name}"


# 🔹 6. Educación del usuario (1-N)
class UserEducation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]
        indexes = [models.Index(fields=["user", "start_date"])]

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("La fecha de fin no puede ser menor que la de inicio")
    def __str__(self):
        return f"{self.title} at {self.institution}"


# 🔹 Modelo para perfiles de CV (con personalización y selección de secciones)
class CVProfile(TimeStampedModel):
    
    SKIN_CHOICES = [
        ('default', 'Clásico'),
        ('modern', 'Moderno'),
        ('minimal', 'Minimalista'),
    ]

    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cv_profiles')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    skin = models.CharField(max_length=50, choices=SKIN_CHOICES, default='default')
    primary_color = models.CharField(max_length=20, default="#000000")
    font_family = models.CharField(max_length=50, default="sans-serif")
    header_image = models.ImageField(upload_to='cv_headers/', blank=True, null=True)
<<<<<<< HEAD
    is_public = models.BooleanField(default=False)
=======
>>>>>>> 78438da6d053703b29f2e02b43b21d9641085c10
    # qr = models.ImageField(upload_to='cv_qr/', blank=True, null=True)
    # pdf = models.FileField(upload_to='cv_pdfs/', blank=True, null=True)
    
    # Relaciones M2M para seleccionar qué datos incluir en el CV
    selected_experiences = models.ManyToManyField(UserJobExperience, blank=True)
    selected_educations = models.ManyToManyField(UserEducation, blank=True)
    selected_softskills = models.ManyToManyField(UserSoftSkill, blank=True)
    selected_hardskills = models.ManyToManyField(UserHardSkill, blank=True)
    selected_languages = models.ManyToManyField(UserLanguage, blank=True)
    selected_hobbies = models.ManyToManyField(UserHobby, blank=True)
    
    class Meta:
        indexes = [models.Index(fields=["user", "slug"])]
    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def save(self, *args, **kwargs):
        # Crear slug único basado en username y título del CV
        if not self.slug:
            base = slugify(f"{self.user.username}-{self.title}")
            slug = base
            i = 1
            while CVProfile.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
