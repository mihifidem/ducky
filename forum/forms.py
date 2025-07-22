from django import forms
from .models import Pregunta, Respuesta, Sector, Profesional

class PreguntaFormPublic(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'pregunta', 'sector']
        widgets = {
            'sector': forms.Select(attrs={
                'class': 'form-control pattern',
                'pattern': '[0-9]',}),
            'pregunta': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PreguntaFormPrivate(forms.ModelForm):

    class Meta:
        model = Pregunta
        fields = ['titulo', 'pregunta',]

    sector = forms.ModelChoiceField(queryset=Sector.objects.all(), required=True)
    profesional = forms.ModelChoiceField(queryset=Profesional.objects.none(), required=True)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'sector' in self.data:
            try:
                sector_id = int(self.data.get('sector'))
                self.fields['profesional'].queryset = Profesional.objects.filter(sector=sector_id)
            except (ValueError, TypeError):
                pass
    


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['respuesta']