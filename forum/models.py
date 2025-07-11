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

class SectoresProfesionales(models.Model):

    sector = models.CharField(max_length=50, choices=Sector.choices, default=Sector.OTRO) 

class Profesional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=100)
    sector = models.ForeignKey(SectoresProfesionales, on_delete=models.CASCADE)
    email2 = models.EmailField()
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Pregunta(models.Model):
    pregunta = models.TextField()
    date_at = models.DateTimeField(auto_now_add=True)
    user_question = models.ForeignKey(User, on_delete=models.CASCADE)
    professional_user = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    sector = models.ForeignKey(SectoresProfesionales, on_delete=models.CASCADE)

    def __str__(self):
        return self.pregunta
    
class Respuesta(models.Model):
    respuesta = models.TextField()
    date_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    user_answer = models.ForeignKey(User, on_delete=models.CASCADE)
    professional_answer = models.ForeignKey(Profesional, on_delete=models.CASCADE)

    def __str__(self):
        return self.respuesta
    
