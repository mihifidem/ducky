from django import forms
from .models import Pregunta, Respuesta, Sector, Profesional

class PreguntaFormPublic(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'pregunta', 'sector']
        widgets = {
            'sector': forms.Select(attrs={
                'class': 'form-control pattern'}),
            'pregunta': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        


class PreguntaFormPrivate(forms.ModelForm):

    class Meta:
        model = Pregunta
        fields = ['titulo', 'pregunta', 'sector', 'professional_user']
        widgets = {
            'sector': forms.Select(attrs={
                'class': 'form-control pattern'}),
            'pregunta': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    professional_user = forms.ModelChoiceField(queryset=Profesional.objects.none(), required=True, label='Profesional')



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'sector' in self.data:
            try:
                sector_id = int(self.data.get('sector'))
                self.fields['professional_user'].queryset = Profesional.objects.filter(sector=sector_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.sector:
            self.fields['professional_user'].queryset = Profesional.objects.filter(sector=self.instance.sector)
    
class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu respuesta aquí...'}),
        }