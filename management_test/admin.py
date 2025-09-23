from django.contrib import admin
from .models import ResultadoTest, PreguntaRespondida, ResultadoInteligencia, ComentariosProfessores

admin.site.register(ResultadoTest)
admin.site.register(PreguntaRespondida)
admin.site.register(ResultadoInteligencia)
admin.site.register(ComentariosProfessores)
