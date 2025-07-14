from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserJobExperience, UserEducation, UserLanguage, UserSoftSkill, UserHobby, UserProfile
from .models import CVProfile



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

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


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Nombre de usuario'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Contraseña'
    }))


class UserJobExperienceForm(forms.ModelForm):
    class Meta:
        model = UserJobExperience
        fields = ['position', 'company', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserEducationForm(forms.ModelForm):
    class Meta:
        model = UserEducation
        fields = ['title', 'institution', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserLanguageForm(forms.ModelForm):
    class Meta:
        model = UserLanguage
        fields = ['language', 'level']


class UserSoftSkillForm(forms.ModelForm):
    class Meta:
        model = UserSoftSkill
        fields = ['skill']

class UserHobbyForm(forms.ModelForm):
    class Meta:
        model = UserHobby
        fields = ['hobby']


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
        
        
# 🔹 CV Profile Form
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
