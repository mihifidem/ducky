from django import forms
from .models import Pregunta, Respuesta

class PreguntaFormPublic(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'pregunta', 'sector']
        widgets = {
            'sector': forms.Select(attrs={'class': 'form-control'}),
            'pregunta': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PreguntaFormPrivate(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'pregunta', 'sector', 'professional_user']


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['respuesta']