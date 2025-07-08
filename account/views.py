# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserJobExperienceForm, UserEducationForm, UserLanguageForm, UserSoftSkillForm, UserHobbyForm, UserProfileForm, UserForm, UserProfileForm
from .models import (UserProfile, UserJobExperience, UserEducation,UserLanguage, UserSoftSkill, UserHobby)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist




def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a login tras registro
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class UserRegisterView(CreateView):
    template_name = 'account/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = CustomAuthenticationForm

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


def profile_view(request):
    return render(request, 'account/profile.html')



@login_required
def add_experience(request):
    if request.method == 'POST':
        form = UserJobExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return redirect('dashboard')
    else:
        form = UserJobExperienceForm()
    
    return render(request, 'account/experience_form.html', {'form': form})



@login_required
def add_education(request):
    if request.method == 'POST':
        form = UserEducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('dashboard')
    else:
        form = UserEducationForm()

    return render(request, 'account/education_form.html', {'form': form})



@login_required
def add_language(request):
    if request.method == 'POST':
        form = UserLanguageForm(request.POST)
        if form.is_valid():
            language = form.save(commit=False)
            language.user = request.user
            language.save()
            return redirect('dashboard')
    else:
        form = UserLanguageForm()

    return render(request, 'account/language_form.html', {'form': form})


@login_required
def add_softskill(request):
    if request.method == 'POST':
        form = UserSoftSkillForm(request.POST)
        if form.is_valid():
            softskill = form.save(commit=False)
            softskill.user = request.user
            softskill.save()
            return redirect('dashboard')
    else:
        form = UserSoftSkillForm()

    return render(request, 'account/softskill_form.html', {'form': form})


@login_required
def add_hobby(request):
    if request.method == 'POST':
        form = UserHobbyForm(request.POST)
        if form.is_valid():
            hobby = form.save(commit=False)
            hobby.user = request.user
            hobby.save()
            return redirect('dashboard')
    else:
        form = UserHobbyForm()

    return render(request, 'account/hobby_form.html', {'form': form})



@login_required
def cv_panel_view(request):
    user = request.user
    try:
        profile = user.userprofile
    except ObjectDoesNotExist:
        return redirect('profile_create')  

    experiences = UserJobExperience.objects.filter(user=user)
    educations = UserEducation.objects.filter(user=user)
    languages = UserLanguage.objects.filter(user=user)
    softskills = UserSoftSkill.objects.filter(user=user)
    hobbies = UserHobby.objects.filter(user=user)

    context = {
        'profile': profile,
        'experiences': experiences,
        'educations': educations,
        'languages': languages,
        'softskills': softskills,
        'hobbies': hobbies,
    }
    return render(request, 'account/cv_panel.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import (
    UserProfile, UserJobExperience, UserEducation,
    UserLanguage, UserSoftSkill, UserHobby
)

@login_required
def dashboard_view(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    context = {
        'profile': profile,
        'experiences': UserJobExperience.objects.filter(user=user),
        'educations': UserEducation.objects.filter(user=user),
        'languages': UserLanguage.objects.filter(user=user),
        'softskills': UserSoftSkill.objects.filter(user=user),
        'hobbies': UserHobby.objects.filter(user=user),
    }

    return render(request, 'account/dashboard.html', context)



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
            return redirect('cv_panel')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'account/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

#  Experience management views

@login_required
def add_experience(request):
    if request.method == "POST":
        form = UserJobExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return redirect('cv_panel')
    else:
        form = UserJobExperienceForm()
    return render(request, 'account/experience_form.html', {'form': form})

@login_required
def edit_experience(request, pk):
    experience = get_object_or_404(UserJobExperience, pk=pk, user=request.user)
    if request.method == "POST":
        form = UserJobExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('cv_panel')
    else:
        form = UserJobExperienceForm(instance=experience)
    return render(request, 'account/experience_form.html', {'form': form})

@login_required
def delete_experience(request, pk):
    experience = get_object_or_404(UserJobExperience, pk=pk, user=request.user)
    if request.method == "POST":
        experience.delete()
        return redirect('cv_panel')
    return render(request, 'account/experience_confirm_delete.html', {'experience': experience})

# Delete Profile View

@login_required
def delete_userprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        # Confirmación recibida, eliminamos solo el perfil
        profile.delete()
        messages.success(request, "Tu perfil ha sido eliminado correctamente.")
        return redirect('cv_panel')  # O la página que desees

    return render(request, 'account/delete_userprofile_confirm.html', {'profile': profile})

# create a new profile view

@login_required
def create_profile_view(request):
    user = request.user
    try:
        # Si ya tiene perfil, redirigir al panel o editar
        if user.userprofile:
            return redirect('cv_panel')
    except Exception:
        pass

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('cv_panel')
    else:
        form = UserProfileForm()

    return render(request, 'account/create_profile.html', {'form': form})