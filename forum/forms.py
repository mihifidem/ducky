from django import forms
from .models import Pregunta, Respuesta

class PreguntaFormPublic(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'pregunta', 'sector']


class PreguntaFormPrivate(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'pregunta', 'sector', 'professional_user']


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['respuesta']