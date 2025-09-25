# Django core imports
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.utils.text import slugify
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from urllib.parse import urlparse, parse_qs

# External libraries
import pdfkit
import os
import zipfile
from datetime import datetime

# Local app: forms
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, UserForm,
 
)

# Local app: models
from .models import (
    UserProfile,
    
)


#------------------------------------------------------------------------------------

# Vista para registro básico de usuario usando UserCreationForm (default)
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a login tras registro
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Vista basada en clase para registro con formulario personalizado
class UserRegisterView(CreateView):
    template_name = 'account/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


# Login y Logout views personalizados para usar formularios propios
class UserLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = CustomAuthenticationForm

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# Vista para mostrar perfil del usuario, solo accesible con login
@login_required
def profile_view(request):
    user = request.user
    # Obtiene perfil del usuario o 404 si no existe
    perfil = get_object_or_404(UserProfile, user=user)
    # Obtiene CVs asociados al usuario
    cvs = CVProfile.objects.filter(user=user)
    return render(request, 'account/profile.html', {'perfil': perfil, 'cvs': cvs})

