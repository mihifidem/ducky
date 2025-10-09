from django import forms
from .models import UserJobExperience, UserEducation, UserLanguage, UserSoftSkill, UserHardSkill, UserHobby, CVProfile, Hobby, SoftSkill, HardSkill
from django.core.exceptions import ValidationError
from django.conf import settings
from .skins import HTML_SKINS

# Formulario para gestionar experiencia laboral de usuario
class UserJobExperienceForm(forms.ModelForm):
    class Meta:
        model = UserJobExperience
        fields = ['position', 'role', 'company', 'start_date', 'end_date', 'description']
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

# Formulario para los Hobbies

class UserHobbyForm(forms.ModelForm):
    hobby_name = forms.CharField(
        label="Hobby",
        required=False,  # ahora opcional
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Correr'}),
        help_text="Solo cambia si quieres modificar el hobby."
    )

    class Meta:
        model = UserHobby
        fields = ['description']  # description sigue siendo obligatorio

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs['instance']
            initial = kwargs.get('initial', {})
            initial['hobby_name'] = instance.hobby.name
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self, user=None, commit=True):
        description = self.cleaned_data.get('description', '').strip()
        hobby_name = self.cleaned_data.get('hobby_name', '').strip()

        # Si no se cambió el hobby, usamos el existente
        if hobby_name:
            hobby, _ = Hobby.objects.get_or_create(name__iexact=hobby_name, defaults={'name': hobby_name})
        else:
            hobby = self.instance.hobby

        # Guardamos el UserHobby
        self.instance.hobby = hobby
        self.instance.description = description
        if commit:
            self.instance.save()
        return self.instance



# Formulario para crear o editar perfiles de CV
# Filtra las opciones de secciones (experiencias, educaciones, etc) para que solo aparezcan las del usuario actual
class CVProfileForm(forms.ModelForm):
    class Meta:
        model = CVProfile
        fields = [
            'title', 'slug', 'skin', 'is_public', 
            'selected_experiences',
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



    def clean_slug(self):
        slug = self.cleaned_data.get("slug")

        reserved = getattr(settings, "RESERVED_SLUGS", ["admin", "api", "cv", "account", "media", "static"])
        if slug in reserved:
            raise ValidationError("❌ Este slug está reservado. Elige otro nombre para tu CV.")

        return slug
    
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

        # Selector visual de skins
        self.fields['skin'].widget = forms.Select(
            choices=[(key, key.capitalize()) for key in HTML_SKINS.keys()]
        )
        # Valor inicial
        self.fields['skin'].initial = self.instance.skin if self.instance else 'default'