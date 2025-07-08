from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Sector(models.TextChoices):
    LEGAL = 'Legal', 'Legal'
    SALUD = 'Salud', 'Salud'
    EDUCACION = 'Educación', 'Educación'
    FINANZAS = 'Finanzas', 'Finanzas'
    GESTION = 'Gestión', 'Gestión'
    PROGRAMACION = 'Programación', 'Programación'
    MARKETING = 'Marketing', 'Marketing'
    OTRO = 'Otro', 'Otro'

class Profesional(User):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    sector = models.CharField(max_length=50, choices=Sector.choices, default=Sector.OTRO)

class Pregunta(models.Model):
    pregunta = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professional_user = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self):
        return self.pregunta[:50] + "..."  # Return the first 50 characters of the question
    
class Respuesta(models.Model):
    respuesta = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professional_user = models.ForeignKey(Profesional, on_delete=models.CASCADE)

    def __str__(self):
        return self.respuesta[:50] + "..."  # Return the first 50 characters of the answer