# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserJobExperienceForm, UserEducationForm, UserLanguageForm, UserSoftSkillForm, UserHobbyForm, UserProfileForm, UserForm, UserProfileForm, UserLanguageForm
from .models import (UserProfile, UserJobExperience, UserEducation, UserLanguage, UserSoftSkill, UserHobby, Language, CVProfile)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import CVProfileForm
from .models import CVProfile
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import uuid
from django.utils.text import slugify
from django.template.loader import render_to_string
import weasyprint




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

# panel view for CV management

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


# Edit Education View

@login_required
def edit_education(request, pk):
    education = get_object_or_404(UserEducation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = UserEducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('cv_panel')
    else:
        form = UserEducationForm(instance=education)
    return render(request, 'account/education_form.html', {'form': form})

@login_required
def delete_education(request, pk):
    education = get_object_or_404(UserEducation, pk=pk, user=request.user)
    if request.method == 'POST':
        education.delete()
        return redirect('cv_panel')
    return render(request, 'account/education_confirm_delete.html', {'education': education})

# leanguage management views

@login_required
def edit_language(request, pk):
    lang = get_object_or_404(UserLanguage, pk=pk, user=request.user)

    if request.method == 'POST':
        form = UserLanguageForm(request.POST, instance=lang)
        if form.is_valid():
            form.save()
            return redirect('cv_panel')
    else:
        form = UserLanguageForm(instance=lang)

    return render(request, 'account/edit_language.html', {'form': form})


@login_required
def delete_language(request, pk):
    language = get_object_or_404(UserLanguage, pk=pk, user=request.user)
    if request.method == 'POST':
        language.delete()
        return redirect('cv_panel')
    return render(request, 'account/language_confirm_delete.html', {'language': language})


# habilidades blandas

@login_required
def edit_softskill(request, pk):
    softskill = get_object_or_404(UserSoftSkill, pk=pk, user=request.user)
    if request.method == 'POST':
        form = UserSoftSkillForm(request.POST, instance=softskill)
        if form.is_valid():
            form.save()
            return redirect('cv_panel')
    else:
        form = UserSoftSkillForm(instance=softskill)
    return render(request, 'account/edit_softskill.html', {'form': form})

@login_required
def delete_softskill(request, pk):
    softskill = get_object_or_404(UserSoftSkill, pk=pk, user=request.user)
    if request.method == 'POST':
        softskill.delete()
        return redirect('cv_panel')
    return render(request, 'account/softskill_confirm_delete.html', {'softskill': softskill})


# hobbies management views

@login_required
def edit_hobby(request, pk):
    hobby = get_object_or_404(UserHobby, pk=pk, user=request.user)
    if request.method == 'POST':
        form = UserHobbyForm(request.POST, instance=hobby)
        if form.is_valid():
            form.save()
            return redirect('cv_panel')
    else:
        form = UserHobbyForm(instance=hobby)
    return render(request, 'account/edit_hobby.html', {'form': form})

@login_required 
def delete_hobby(request, pk):
    hobby = get_object_or_404(UserHobby, pk=pk, user=request.user)
    if request.method == 'POST':
        hobby.delete()
        return redirect('cv_panel')
    return render(request, 'account/hobby_confirm_delete.html', {'hobby': hobby})


# CV Profile management views


@login_required
def create_cv(request):
    if request.method == 'POST':
        form = CVProfileForm(request.POST, user=request.user)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()
            form.save_m2m()
            return redirect('cv_list')
    else:
        form = CVProfileForm(user=request.user)
        
    return render(request, 'account/cv_form.html', {'form': form})



@login_required
def cv_list(request):
    cvs = request.user.cv_profiles.all()
    return render(request, 'account/cv_list.html', {'cvs': cvs})


@login_required
def cv_create(request):
	if request.method == 'POST':
		form = CVProfileForm(request.POST)
		if form.is_valid():
			cv = form.save(commit=False)
			cv.user = request.user
			cv.slug = slugify(f"{request.user.username}_{cv.title}")
			cv.save()
			form.save_m2m()
			return redirect('cv_list')
	else:
		form = CVProfileForm()
	return render(request, 'account/cv_form.html', {'form': form})

@login_required
def cv_edit(request, pk):
	cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
	form = CVProfileForm(request.POST or None, instance=cv)
	if form.is_valid():
		form.save()
		return redirect('cv_list')
	return render(request, 'account/cv_form.html', {'form': form})

@login_required
def cv_delete(request, pk):
	cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
	if request.method == 'POST':
		cv.delete()
		return redirect('cv_list')
	return render(request, 'account/cv_confirm_delete.html', {'cv': cv})

@login_required
def cv_clone(request, pk):
	cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
	clone = CVProfile.objects.create(
		user=request.user,
		title=cv.title + " (copia)",
		slug=slugify(f"{cv.slug}_copy"),
		skin=cv.skin
	)
	clone.selected_experiences.set(cv.selected_experiences.all())
	clone.selected_educations.set(cv.selected_educations.all())
	clone.selected_softskills.set(cv.selected_softskills.all())
	clone.selected_languages.set(cv.selected_languages.all())
	clone.selected_hobbies.set(cv.selected_hobbies.all())
	return redirect('cv_list')


# Vista para previsualizar el CV

def preview_cv(request, slug):
    cv = get_object_or_404(CVProfile, slug=slug)
    template_map = {
        'default': 'account/skins/cv_default.html',
        'modern': 'account/skins/cv_modern.html',
        'minimal': 'account/skins/cv_minimal.html',
    }
    template_path = template_map.get(cv.skin, 'account/skins/cv_default.html')
    return render(request, template_path, {'cv': cv})



# Vista para ver el CV en PDF

def generate_cv_pdf(request, slug):
    # Buscar el CV por slug
    cv = get_object_or_404(CVProfile, slug=slug)
    
    # Mapeo de skins a templates
    template_map = {
        'default': 'account/skins/pdf/cv_default_pdf.html',
        'modern': 'account/skins/pdf/cv_modern_pdf.html',
        'minimal': 'account/skins/pdf/cv_minimal_pdf.html',
    }

    # Selección del template
    template_path = template_map.get(cv.skin, 'account/skins/pdf/cv_default_pdf.html')
    template = get_template(template_path)
    
    # Renderizar el HTML con el contexto
    html = template.render({'cv': cv})

    # Crear respuesta como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.slug}.pdf"'

    # Generar PDF desde HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Comprobar errores
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response

# Vista cv Public

def cv_public_view(request, slug):
    cv = get_object_or_404(CVProfile, slug=slug)
    return render(request, f'account/skins/cv_{cv.skin}.html', {'cv': cv})

# exportar pdf

def cv_download_pdf(request, pk):
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    
    html = render_to_string(f'accounts/cv/skins/{cv.skin}.html', {'cv': cv})
    
    pdf = weasyprint.HTML(string=html).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.slug}.pdf"'
    
    return response

# cv vista lista

@login_required
def cv_list_view(request):
    cvs = CVProfile.objects.filter(user=request.user)
    return render(request, 'account/skins/cv_list.html', {'cvs': cvs})
