from django.contrib import admin
from .models import Pregunta, Respuesta, Profesional, Sector

# Register your models here.
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(Profesional)
admin.site.register(Sector)