from django import forms
from .models import UserJobExperience, UserEducation, UserLanguage, UserSoftSkill, UserHardSkill, UserHobby, CVProfile, Hobby, SoftSkill, HardSkill
from django.core.exceptions import ValidationError


# Formulario para gestionar experiencia laboral de usuario
class UserJobExperienceForm(forms.ModelForm):
    class Meta:
        model = UserJobExperience
        fields = ['position', 'company', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),  # Calendario para fechas
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Formulario para gestionar educación del usuario
class UserEducationForm(forms.ModelForm):
    class Meta:
        model = UserEducation
        fields = ['title', 'institution', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Formulario para agregar idiomas al perfil, con validación para evitar duplicados
class UserLanguageForm(forms.ModelForm):
    class Meta:
        model = UserLanguage
        fields = ['language', 'level']
        widgets = {
            'language': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Recibe el usuario para validar que no duplique idiomas
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        language = cleaned_data.get('language')

        # Verifica si el idioma ya existe para ese usuario, excepto si es la instancia actual (edición)
        if self.user and language:
            existing = UserLanguage.objects.filter(user=self.user, language=language)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError("Este idioma ya ha sido añadido.")

        return cleaned_data    


# Formulario para habilidades blandas (soft skills)
class UserSoftSkillForm(forms.Form):
    skill = forms.CharField(
        label="Habilidad blanda",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Trabajo en equipo'}),
        help_text="Escribe una habilidad blanda. Se creará si no existe."
    )

    def save(self, user):
        skill_name = self.cleaned_data['skill'].strip()

        # Busca la habilidad (ignorando mayúsculas/minúsculas)
        skill = SoftSkill.objects.filter(name__iexact=skill_name).first()

        if not skill:
            skill = SoftSkill.objects.create(name=skill_name)

        # Evita duplicados
        user_skill, created = UserSoftSkill.objects.get_or_create(user=user, skill=skill)
        return user_skill

# Formulario para habilidades duras (hard skills)
class UserHardSkillForm(forms.Form):
    skill = forms.CharField(
        label="Habilidad dura",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Python'}),
        help_text="Escribe una habilidad dura. Se creará si no existe."
    )

    def save(self, user):
        skill_name = self.cleaned_data['skill'].strip()

        # Busca la habilidad (ignorando mayúsculas/minúsculas)
        skill = HardSkill.objects.filter(name__iexact=skill_name).first()

        if not skill:
            skill = HardSkill.objects.create(name=skill_name)

        # Evita duplicados
        user_skill, created = UserHardSkill.objects.get_or_create(user=user, skill=skill)
        return user_skill

# Formulario para hobbies
class UserHobbyForm(forms.Form):
    hobby = forms.CharField(
        label="Hobby",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Escalar'}),
        help_text="Escribe un hobby. Se creará si no existe."
    )

    def save(self, user):
        hobby_name = self.cleaned_data['hobby'].strip()

        # Buscar con name__iexact (case-insensitive)
        hobby = Hobby.objects.filter(name__iexact=hobby_name).first()

        if not hobby:
            hobby = Hobby.objects.create(name=hobby_name)

        # Evita duplicados
        user_hobby, created = UserHobby.objects.get_or_create(user=user, hobby=hobby)
        return user_hobby




# Formulario para crear o editar perfiles de CV
# Filtra las opciones de secciones (experiencias, educaciones, etc) para que solo aparezcan las del usuario actual
class CVProfileForm(forms.ModelForm):
    class Meta:
        model = CVProfile
        fields = [
            'title', 'skin', 'selected_experiences',
            'selected_educations',
            'selected_softskills', 'selected_hardskills', 
            'selected_languages',
            'selected_hobbies'
        ]
        widgets = {
            'selected_experiences': forms.CheckboxSelectMultiple(),
            'selected_educations': forms.CheckboxSelectMultiple(),
            'selected_softskills': forms.CheckboxSelectMultiple(),
            'selected_hardskills': forms.CheckboxSelectMultiple(),
            'selected_languages': forms.CheckboxSelectMultiple(),
            'selected_hobbies': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Captura el usuario para filtrar queryset
        super().__init__(*args, **kwargs)
        if user:
            self.fields['selected_experiences'].queryset = UserJobExperience.objects.filter(user=user)
            self.fields['selected_educations'].queryset = UserEducation.objects.filter(user=user)
            self.fields['selected_softskills'].queryset = UserSoftSkill.objects.filter(user=user)
            self.fields['selected_hardskills'].queryset = UserHardSkill.objects.filter(user=user)
            self.fields['selected_languages'].queryset = UserLanguage.objects.filter(user=user)
            self.fields['selected_hobbies'].queryset = UserHobby.objects.filter(user=user)
