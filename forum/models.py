from django.db import models
from django.contrib.auth.models import User
from dirtyfields import DirtyFieldsMixin

# Create your models here.

class Sector(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre



class Profesional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=100)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    email2 = models.EmailField()
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.user.username



class Pregunta(DirtyFieldsMixin,models.Model):
    titulo = models.CharField(max_length=200, default='')
    pregunta = models.TextField(default='')
    date_at = models.DateTimeField(auto_now_add=True)
    user_question = models.ForeignKey(User, on_delete=models.CASCADE)
    professional_user = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:  # Es edición
            dirty_fields = self.get_dirty_fields()
            if dirty_fields:
                self.edited = True
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.is_public == False and not self.professional_user:
            raise ValidationError("Debe seleccionar un profesional si la pregunta no es pública.")

    def __str__(self):
        return self.pregunta
    
class Respuesta(models.Model):
    respuesta = models.TextField()
    date_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    user_answer = models.ForeignKey(User, on_delete=models.CASCADE)
    professional_answer = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.respuesta
    
