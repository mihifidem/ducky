# Django core imports
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
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
from datetime import datetime

# Local app: forms
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, UserForm
 
)

# Local app: models
from .models import (
    UserProfile,
    
)

# ----------------------
# Registro y Autenticación
# ------------------------

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

# ------------------------
# Perfil de Usuario
# ------------------------

# Vista para mostrar perfil del usuario, solo accesible con login
@login_required
def profile_view(request):
    user = request.user
    perfil = get_object_or_404(UserProfile, user=user)
    return render(request, 'account/profile.html', {'perfil': perfil})


@login_required
def edit_profile(request):
    user = request.user
    profile = user.userprofile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    return render(request, 'account/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def delete_userprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, "Tu perfil ha sido eliminado correctamente.")
        return redirect('profile')
    return render(request, 'account/delete_userprofile_confirm.html', {'profile': profile})

@login_required
def create_profile_view(request):
    user = request.user
    try:
        if user.userprofile:
            return redirect('profile')
    except Exception:
        pass

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm()

    return render(request, 'account/create_profile.html', {'form': form})
