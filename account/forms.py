from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserJobExperience, UserEducation, UserLanguage, UserSoftSkill, UserHobby, UserProfile, CVProfile, Hobby, SoftSkill
from django.core.exceptions import ValidationError


# Formulario para editar campos básicos de User
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

# Formulario personalizado para registro de usuario con email obligatorio
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repetir contraseña'}),
        }


# Formulario personalizado para login con placeholders y clases CSS para mejor UI
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Nombre de usuario'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Contraseña'
    }))


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

# Formulario para editar perfil de usuario, con widgets para mejorar la UI
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'phone', 'birthdate', 'address', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# Formulario para crear o editar perfiles de CV
# Filtra las opciones de secciones (experiencias, educaciones, etc) para que solo aparezcan las del usuario actual
class CVProfileForm(forms.ModelForm):
    class Meta:
        model = CVProfile
        fields = [
            'title', 'skin', 'selected_experiences',
            'selected_educations',
            'selected_softskills', 'selected_languages',
            'selected_hobbies'
        ]
        widgets = {
            'selected_experiences': forms.CheckboxSelectMultiple(),
            'selected_educations': forms.CheckboxSelectMultiple(),
            'selected_softskills': forms.CheckboxSelectMultiple(),
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
            self.fields['selected_languages'].queryset = UserLanguage.objects.filter(user=user)
            self.fields['selected_hobbies'].queryset = UserHobby.objects.filter(user=user)
