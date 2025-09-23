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
    CustomUserCreationForm, CustomAuthenticationForm, UserJobExperienceForm,
    UserEducationForm, UserLanguageForm, UserSoftSkillForm, UserHobbyForm,
    UserProfileForm, UserForm, CVProfileForm
)

# Local app: models
from .models import (
    UserProfile, UserJobExperience, UserEducation, UserLanguage,
    UserSoftSkill, UserHobby, Language, CVProfile, Hobby
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

# Funciones para añadir experiencias, educación, idiomas, habilidades blandas y hobbies.

@login_required
def add_experience(request):
    if request.method == 'POST':
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
def add_education(request):
    if request.method == 'POST':
        form = UserEducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('cv_panel')  # Igual aquí
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
            return redirect('cv_panel')  # Igual aquí
    else:
        form = UserLanguageForm()
    return render(request, 'account/language_form.html', {'form': form})


@login_required
def add_softskill(request):
    if request.method == 'POST':
        form = UserSoftSkillForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('cv_panel')  
    else:
        form = UserSoftSkillForm()

    return render(request, 'account/softskill_form.html', {'form': form})
    

@login_required
def add_hobby(request):
    if request.method == 'POST':
        form = UserHobbyForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('cv_panel') 
    else:
        form = UserHobbyForm()
    return render(request, 'account/hobby_form.html', {'form': form})

# Vista para mostrar el panel principal de CVs y datos relacionados
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
    
    # Filtrar solo los CVs del usuario actual
    cvs = CVProfile.objects.filter(user=user)

    context = {
        'profile': profile,
        'experiences': experiences,
        'educations': educations,
        'languages': languages,
        'softskills': softskills,
        'hobbies': hobbies,
        'cvs': cvs,
    }

    return render(request, 'account/cv_panel.html', context)

# Vista para el dashboard, con datos similares al panel pero quizás menos detallado
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



# Vista para editar perfil usuario, incluye edición de User y UserProfile
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



# Manejo de experiencias: añadir, editar, eliminar (muy similar a añadir experiencia anterior)
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


# Vista para eliminar el perfil del usuario (solo perfil, no el usuario)
@login_required
def delete_userprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        profile.delete()
        messages.success(request, "Tu perfil ha sido eliminado correctamente.")
        return redirect('cv_panel')

    return render(request, 'account/delete_userprofile_confirm.html', {'profile': profile})


# Crear nuevo perfil (si no tiene)
@login_required
def create_profile_view(request):
    user = request.user
    try:
        # Si ya tiene perfil, redirigir al panel
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
        form = CVProfileForm(user=request.user)

    return render(request, 'account/create_profile.html', {'form': form})


# Editar educación y eliminar educación
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


# Manejo idiomas: añadir, editar, eliminar, con control para evitar duplicados y actualizar nivel
@login_required
def add_language(request):
    if request.method == 'POST':
        form = UserLanguageForm(request.POST, user=request.user)
        if form.is_valid():
            language_obj = form.cleaned_data['language']
            level = form.cleaned_data['level']

            obj, created = UserLanguage.objects.get_or_create(
                user=request.user,
                language=language_obj,
                defaults={'level': level}
            )

            if not created and obj.level != level:
                obj.level = level
                obj.save()

            return redirect('cv_panel')
    else:
        form = UserLanguageForm(user=request.user)
    return render(request, 'account/language_form.html', {'form': form})

@login_required
def edit_language(request, pk):
    language_instance = get_object_or_404(UserLanguage, pk=pk)
    if request.method == 'POST':
        form = UserLanguageForm(request.POST, instance=language_instance, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('cv_panel')
    else:
        form = UserLanguageForm(instance=language_instance, user=request.user)
    return render(request, 'account/edit_language.html', {'form': form})

@login_required
def delete_language(request, pk):
    if request.method == "POST":
        language = get_object_or_404(UserLanguage, pk=pk)
        language.delete()
    return redirect('cv_panel')


# Edición y eliminación habilidades blandas
@login_required
def edit_softskill(request, pk):
    user_softskill = get_object_or_404(UserSoftSkill, pk=pk, user=request.user)

    if request.method == 'POST':
        form = UserSoftSkillForm(request.POST)
        if form.is_valid():
            # Borramos la anterior
            user_softskill.delete()
            # Creamos la nueva
            form.save(user=request.user)
            return redirect('cv_panel')
    else:
        form = UserSoftSkillForm(initial={'skill': user_softskill.skill.name})

    return render(request, 'account/edit_softskill.html', {'form': form, 'user_softskill': user_softskill})


@login_required
def delete_softskill(request, pk):
    softskill = get_object_or_404(UserSoftSkill, pk=pk, user=request.user)
    if request.method == 'POST':
        softskill.delete()
        return redirect('cv_panel')
    return render(request, 'account/softskill_confirm_delete.html', {'softskill': softskill})



# Edición y eliminación hobbies
@login_required
def edit_hobby(request, pk):
    user_hobby = get_object_or_404(UserHobby, pk=pk, user=request.user)

    if request.method == 'POST':
        form = UserHobbyForm(request.POST)
        if form.is_valid():
            hobby_name = form.cleaned_data['hobby'].strip()
            hobby = Hobby.objects.filter(name__iexact=hobby_name).first()
            if not hobby:
                hobby = Hobby.objects.create(name=hobby_name)
            user_hobby.hobby = hobby
            user_hobby.save()
            return redirect('cv_panel')
    else:
        form = UserHobbyForm(initial={'hobby': user_hobby.hobby.name})

    return render(request, 'account/edit_hobby.html', {'form': form})

@login_required
def delete_hobby(request, pk):
    hobby_relation = get_object_or_404(UserHobby, pk=pk, user=request.user)
    if request.method == 'POST':
        hobby = hobby_relation.hobby
        hobby_relation.delete()
        # Verificar si el hobby quedó huérfano (sin usuarios)
        if not UserHobby.objects.filter(hobby=hobby).exists():
            hobby.delete()
        return redirect('cv_panel')
    return render(request, 'account/hobby_confirm_delete.html', {'hobby': hobby_relation})


# CV Management views: crear, listar, editar, eliminar, clonar

@login_required
def cv_create(request):
    profile = UserProfile.objects.filter(user=request.user).first()

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

    return render(request, 'account/cv_form.html', {
        'form': form,
        'profile': profile
    })


@login_required
def cv_list(request):
    cvs = request.user.cv_profiles.all()
    return render(request, 'account/cv_list.html', {'cvs': cvs})


@login_required
def cv_edit(request, pk):
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CVProfileForm(request.POST, instance=cv, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('cv_list')
    else:
        form = CVProfileForm(instance=cv, user=request.user)
    return render(request, 'account/cv_form.html', {'form': form})

@login_required
def cv_delete(request, pk):
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        cv.delete()
        messages.success(request, "CV eliminado correctamente.")
        return redirect('cv_list')
    return render(request, 'account/cv_confirm_delete.html', {'cv': cv})

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify
from .models import CVProfile

@login_required
def cv_clone(request, pk):
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)

    base_slug = slugify(f"{cv.slug}_copia")
    new_title = f"{cv.title} (copia)"
    new_slug = base_slug
    counter = 1

    while CVProfile.objects.filter(slug=new_slug).exists():
        counter += 1
        new_slug = f"{base_slug}_{counter}"
        new_title = f"{cv.title} (copia {counter})"

    clone = CVProfile.objects.create(
        user=request.user,
        title=new_title,
        slug=new_slug,
        created_at=cv.created_at,
        skin=cv.skin
    )

    clone.selected_experiences.set(cv.selected_experiences.all())
    clone.selected_educations.set(cv.selected_educations.all())
    clone.selected_softskills.set(cv.selected_softskills.all())
    clone.selected_languages.set(cv.selected_languages.all())
    clone.selected_hobbies.set(cv.selected_hobbies.all())

    messages.success(request, f'CV clonado correctamente como “{new_title}”.')
    return redirect(f"{reverse('cv_list')}?clonado={clone.pk}&origen={cv.pk}")


# Vista para previsualizar el CV en formato HTML según el skin seleccionado
def preview_cv(request, slug):
    cv = get_object_or_404(CVProfile, slug=slug)

    # Diccionario para mapear el tipo de skin con su template correspondiente
    template_map = {
        'default': 'account/skins/cv_default.html',
        'modern': 'account/skins/cv_modern.html',
        'minimal': 'account/skins/cv_minimal.html',
    }

    # Si el skin no está en el mapa, se usa 'default'
    template_path = template_map.get(cv.skin, 'account/skins/cv_default.html')

    return render(request, template_path, {'cv': cv})



# Vista pública para mostrar el CV según su skin
def cv_public_view(request, slug):
    cv = get_object_or_404(CVProfile, slug=slug)
    profile = UserProfile.objects.filter(user=cv.user).first()  # Obtener perfil del dueño del CV

    return render(request, f'account/skins/cv_{cv.skin}.html', {
        'cv': cv,
        'profile': profile,  # Pasamos profile para usar en la plantilla
    })



# Vista para listar todos los CVs del usuario autenticado
@login_required
def cv_list_view(request):
    cvs = CVProfile.objects.filter(user=request.user)
    return render(request, 'account/cv_list.html', {'cvs': cvs})



# Vista para descargar el CV en PDF desde una web publica con pdfkit
@login_required
def cv_download_pdf(request, slug):
    # Obtener el CV del usuario
    cv = get_object_or_404(CVProfile, slug=slug, user=request.user)

    # Obtener el perfil del usuario
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    # Plantillas según el skin
    template_map = {
        'default': 'account/skins/pdf/cv_default_pdf.html',
        'modern': 'account/skins/pdf/cv_modern_pdf.html',
        'minimal': 'account/skins/pdf/cv_minimal_pdf.html',
    }
    template_path = template_map.get(cv.skin, 'account/skins/pdf/cv_default_pdf.html')

    # Renderizar HTML con cv y profile
    context = {
        'cv': cv,
        'profile': profile,
    }
    html = render_to_string(template_path, context, request=request)

    # Configurar wkhtmltopdf
    path_wkhtmltopdf = r'C:\Archivos de programa\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Crear PDF
    pdf = pdfkit.from_string(html, False, configuration=config)

    # Devolver respuesta PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.slug}.pdf"'
    return response



# Vista para descargar los pdf seleccionados en ZIP
@login_required
def download_selected_cvs(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_cvs')
        cvs = CVProfile.objects.filter(id__in=selected_ids)

        # Ruta wkhtmltopdf en Windows
        path_wkhtmltopdf = r'C:\Archivos de programa\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        # Crear carpeta destino para el ZIP
        zip_dir = os.path.join(settings.MEDIA_ROOT, 'cv_zips')
        os.makedirs(zip_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_filename = f'CVs_Seleccionados_{timestamp}.zip'
        zip_path = os.path.join(zip_dir, zip_filename)

        # Mapeo de skins a plantillas
        template_map = {
            'default': 'account/skins/pdf/cv_default_pdf.html',
            'modern': 'account/skins/pdf/cv_modern_pdf.html',
            'minimal': 'account/skins/pdf/cv_minimal_pdf.html',
        }

        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for cv in cvs:
                # Obtener plantilla correspondiente al skin
                template_path = template_map.get(cv.skin, template_map['default'])

                # Obtener el perfil del usuario del CV
                try:
                    profile = cv.user.userprofile  # o cv.user.profile según tu modelo
                except UserProfile.DoesNotExist:
                    profile = None

                context = {
                    'cv': cv,
                    'profile': profile,
                }

                html = render_to_string(template_path, context)

                pdf_file = pdfkit.from_string(html, False, configuration=config)

                safe_title = slugify(cv.title)
                filename = f"{safe_title}_{cv.user.username}.pdf"
                zip_file.writestr(filename, pdf_file)

        return redirect(f"{settings.MEDIA_URL}cv_zips/{zip_filename}")

    return HttpResponse("Método no permitido", status=405)


# vista error 404

def page_not_found_view(request, exception):
    return render(request, 'account/404.html', status=404)

# URL desconfigurada

def mi_vista(request):
    url_completa = request.build_absolute_uri()
    partes = urlparse(url_completa)

    contexto = {
        'url_completa': url_completa,
        'esquema': partes.scheme,
        'dominio': partes.netloc,
        'ruta': partes.path,
        'parametros': partes.params,
        'query_string': partes.query,
        'fragmento': partes.fragment,
        'query_dict': parse_qs(partes.query)
    }

    return render(request, 'account/info_url.html', contexto)
