# Django core imports
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.utils.text import slugify
from django.conf import settings
from urllib.parse import urlparse, parse_qs
from .models import CVProfile
from account.cv_manager.models import UserJobExperience

# External libraries
import pdfkit
import os
import zipfile
from datetime import datetime
from django.db.models import Q

# Formularios
from .forms import (
    UserJobExperienceForm, CVProfileForm, 
    UserEducationForm, UserLanguageForm, UserSoftSkillForm, 
    UserHardSkillForm, UserHobbyForm,
)

from account.forms import UserForm

# Modelos
from .models import (
    UserJobExperience, UserEducation, UserLanguage,
    UserSoftSkill, UserHobby, Language, CVProfile, Hobby,
    UserHardSkill
)

from account.models import UserProfile

# Función para manejar el error 404
def cv_not_found_handler(request, exception):
    return render(request, "cv_manager/404.html", status=404)

# ------------------------
# Panel y Dashboard
# ------------------------

# Vista para mostrar el panel principal de CVs y datos relacionados
@login_required
def cv_panel_view(request):
    user = request.user
    try:
        profile = user.userprofile
    except ObjectDoesNotExist:
        return redirect('profile_create')

    # Obtener CVs, experiencias, educaciones, idiomas, habilidades blandas y hobbies
    experiences = UserJobExperience.objects.filter(user=user)
    educations = UserEducation.objects.filter(user=user)
    languages = UserLanguage.objects.filter(user=user)
    softskills = UserSoftSkill.objects.filter(user=user)
    hardskills = UserHardSkill.objects.filter(user=user)
    hobbies = UserHobby.objects.filter(user=user)
    
    # Optimizar consultas de CVProfile con relaciones ManyToMany y evitar muchas consultas
    cvs = CVProfile.objects.filter(user=user).prefetch_related(
        'selected_experiences',
        'selected_educations',
        'selected_languages',
        'selected_softskills',
        'selected_hardskills',
        'selected_hobbies'
    )

    context = {
        'profile': profile,
        'experiences': experiences,
        'educations': educations,
        'languages': languages,
        'softskills': softskills,
        'hardskills': hardskills,
        'hobbies': hobbies,
        'cvs': cvs,
    }

    return render(request, 'cv_manager/cv_panel.html', context)


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
        'hardskills': UserHardSkill.objects.filter(user=user),
        'hobbies': UserHobby.objects.filter(user=user),
    }
    return render(request, 'cv_manager/dashboard.html', context)

# ------------------------
# CRUD Experiencias
# ------------------------


# Funciones para añadir experiencias, educación, idiomas, habilidades blandas y hobbies.
@login_required
def add_experience(request):
    if request.method == 'POST':
        form = UserJobExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return redirect('experience_list')  
    else:
        form = UserJobExperienceForm()
    return render(request, 'cv_manager/experience_form.html', {'form': form})


# Enlace a Experience_list

@login_required
def experience_list(request):
    queryset = UserJobExperience.objects.filter(user=request.user)  # Solo experiencias del usuario logueado
    
    # 🔹 Filtro por palabra clave (position, company, role, description)
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(position__icontains=search) |
            Q(company__icontains=search) |
            Q(role__icontains=search) |
            Q(description__icontains=search)
        )
    
    # 🔹 Filtro por fechas
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        queryset = queryset.filter(start_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(end_date__lte=end_date)

    context = {
        'experiences': queryset,
        'search': search,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'cv_manager/experience_list.html', context)
    
# Manejo de experiencias: añadir, editar, eliminar (muy similar a añadir experiencia anterior)
@login_required
def edit_experience(request, pk):
    experience = get_object_or_404(UserJobExperience, pk=pk, user=request.user)
    if request.method == "POST":
        form = UserJobExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('experience_list')
    else:
        form = UserJobExperienceForm(instance=experience)
    return render(request, 'cv_manager/experience_form.html', {'form': form})


@login_required
def delete_experience(request, pk):
    experience = get_object_or_404(UserJobExperience, pk=pk, user=request.user)
    if request.method == "POST":
        experience.delete()
        return redirect('experience_list')
    return render(request, 'cv_manager/experience_confirm_delete.html', {'experience': experience})


# ------------------------
# CRUD Educación
# ------------------------


# Funciones para añadir educación.
@login_required
def add_education(request):
    if request.method == 'POST':
        form = UserEducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('education_list')  # Igual aquí
    else:
        form = UserEducationForm()
    return render(request, 'cv_manager/education_form.html', {'form': form})


# Enlace a Education_list
@login_required
def education_list(request):
    queryset = UserEducation.objects.filter(user=request.user)
    
    # 🔹 Búsqueda por palabra clave (title, institution, description)
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(institution__icontains=search) |
            Q(description__icontains=search)
        )

    # 🔹 Filtro por fechas
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        queryset = queryset.filter(start_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(end_date__lte=end_date)

    context = {
        'educations': queryset,
        'search': search,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'cv_manager/education_list.html', context)

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
    return render(request, 'cv_manager/education_form.html', {'form': form})

@login_required
def delete_education(request, pk):
    education = get_object_or_404(UserEducation, pk=pk, user=request.user)
    if request.method == 'POST':
        education.delete()
        return redirect('cv_panel')
    return render(request, 'cv_manager/education_confirm_delete.html', {'education': education})

# ------------------------
# CRUD Idiomas
# ------------------------


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

            return redirect('language_list')
    else:
        form = UserLanguageForm(user=request.user)
    return render(request, 'cv_manager/language_form.html', {'form': form})

# Listado de idiomas
@login_required
def language_list(request):
    # 🔹 Solo los idiomas del usuario logueado
    queryset = UserLanguage.objects.filter(user=request.user)

    # 🔹 Filtro por palabra clave en el nombre del idioma
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(language__name__icontains=search)
        )

    # 🔹 Filtro por nivel
    level = request.GET.get('level', '')
    if level:
        queryset = queryset.filter(level=level)

    context = {
        'languages': queryset,
        'search': search,
        'level': level,
    }
    return render(request, 'cv_manager/language_list.html', context)

@login_required
def edit_language(request, pk):
    language_instance = get_object_or_404(UserLanguage, pk=pk)
    if request.method == 'POST':
        form = UserLanguageForm(request.POST, instance=language_instance, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('language_list')
    else:
        form = UserLanguageForm(instance=language_instance, user=request.user)
    return render(request, 'cv_manager/edit_language.html', {'form': form})

@login_required
def delete_language(request, pk):
    language = get_object_or_404(UserLanguage, pk=pk)  # definir siempre

    if request.method == "POST":
        language.delete()
        return redirect('language_list')

    # Para GET, mostrar página de confirmación
    return render(request, 'cv_manager/language_confirm_delete.html', {'language': language})

# ------------------------
# CRUD Soft Skills
# ------------------------

# Funciones para añadir soft skills.

@login_required
def add_softskill(request):
    if request.method == 'POST':
        form = UserSoftSkillForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('softskill_list')  
    else:
        form = UserSoftSkillForm()

    return render(request, 'cv_manager/softskill_form.html', {'form': form})

# Listado de habilidades blandas (Soft Skills)
@login_required
def softskill_list(request):
    # 🔹 Solo las soft skills del usuario logueado
    queryset = UserSoftSkill.objects.filter(user=request.user)

    # 🔹 Filtro por palabra clave en el nombre de la habilidad
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(skill__name__icontains=search)
        )

    context = {
        'softskills': queryset,
        'search': search,
    }
    return render(request, 'cv_manager/softskill_list.html', context)

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
            return redirect('softskill_list')
    else:
        form = UserSoftSkillForm(initial={'skill': user_softskill.skill.name})

    return render(request, 'cv_manager/edit_softskill.html', {'form': form, 'user_softskill': user_softskill})


@login_required
def delete_softskill(request, pk):
    softskill = get_object_or_404(UserSoftSkill, pk=pk, user=request.user)
    if request.method == 'POST':
        softskill.delete()
        return redirect('softskill_list')
    return render(request, 'cv_manager/softskill_confirm_delete.html', {'softskill': softskill})

# ------------------------
# CRUD Hard Skills
# ------------------------

# Funciones para añadir hardskills.
@login_required
def add_hardskill(request):
    if request.method == 'POST':
        form = UserHardSkillForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('hardskill_list') 
    else:
        form = UserHardSkillForm()
    return render(request, 'cv_manager/hardskill_form.html', {'form': form})
    

# Listado de habilidades fuertes (Hard Skills)
@login_required
def hardskill_list(request):
    # 🔹 Solo las habilidades fuertes del usuario
    queryset = UserHardSkill.objects.filter(user=request.user)

    # 🔹 Filtro por palabra clave en el nombre de la habilidad
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(skill__name__icontains=search)
        )

    context = {
        'hardskills': queryset,
        'search': search,
    }
    return render(request, 'cv_manager/hardskill_list.html', context)


# Edición y eliminación habilidades fuertes
def edit_hardskill(request, pk):
    user_hardskill = get_object_or_404(UserHardSkill, pk=pk, user=request.user)

    if request.method == 'POST':
        form = UserHardSkillForm(request.POST)
        if form.is_valid():
            # Borramos la anterior
            user_hardskill.delete()
            # Creamos la nueva
            form.save(user=request.user)
            return redirect('hardskill_list')
    else:
        form = UserHardSkillForm(initial={'skill': user_hardskill.skill.name})

    return render(request, 'cv_manager/edit_hardskill.html', {'form': form, 'user_hardskill': user_hardskill})

@login_required
def delete_hardskill(request, pk):
    hardskill = get_object_or_404(UserHardSkill, pk=pk, user=request.user)
    if request.method == 'POST':
        hardskill.delete()
        return redirect('hardskill_list')
    return render(request, 'cv_manager/hardskill_confirm_delete.html', {'hardskill': hardskill})

# ------------------------
# CRUD Hobbies
# ------------------------

# Funciones para añadir hobbies.

@login_required
def add_hobby(request):
    if request.method == 'POST':
        form = UserHobbyForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('hobby_list') 
    else:
        form = UserHobbyForm()
    return render(request, 'cv_manager/hobby_form.html', {'form': form})


# Listado de hobbies
@login_required
def hobby_list(request):
    # 🔹 Solo hobbies del usuario logueado
    queryset = UserHobby.objects.filter(user=request.user)

    # 🔹 Filtro por palabra clave en el nombre del hobby o descripción
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(hobby__name__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'hobbies': queryset,
        'search': search,
    }
    return render(request, 'cv_manager/hobby_list.html', context)

    
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
            return redirect('hobby_list')
    else:
        form = UserHobbyForm(initial={'hobby': user_hobby.hobby.name})

    return render(request, 'cv_manager/edit_hobby.html', {'form': form})

@login_required
def delete_hobby(request, pk):
    hobby_relation = get_object_or_404(UserHobby, pk=pk, user=request.user)
    if request.method == 'POST':
        hobby = hobby_relation.hobby
        hobby_relation.delete()
        # Verificar si el hobby quedó huérfano (sin usuarios)
        if not UserHobby.objects.filter(hobby=hobby).exists():
            hobby.delete()
        return redirect('hobby_list')
    return render(request, 'cv_manager/hobby_confirm_delete.html', {'hobby': hobby_relation})


# ------------------------
# CRUD CVProfile
# ------------------------

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

    return render(request, 'cv_manager/cv_form.html', {
        'form': form,
        'profile': profile
    })


@login_required
def cv_list(request):
    cvs = request.user.cv_profiles.all()
    return render(request, 'cv_manager/cv_list.html', {'cvs': cvs})


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
    return render(request, 'cv_manager/cv_form.html', {'form': form})

@login_required
def cv_delete(request, pk):
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        cv.delete()
        messages.success(request, "CV eliminado correctamente.")
        return redirect('cv_list')
    return render(request, 'cv_manager/cv_confirm_delete.html', {'cv': cv})



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

# ------------------------
# Previsualización y vista pública
# ------------------------


# Vista para previsualizar el CV en formato HTML según el skin seleccionado
def preview_cv(request, slug):
    cv = get_object_or_404(CVProfile, slug=slug)

    # Diccionario para mapear el tipo de skin con su template correspondiente
    template_map = {
        'default': 'cv_manager/skins/cv_default.html',
        'modern': 'cv_manager/skins/cv_modern.html',
        'minimal': 'cv_manager/skins/cv_minimal.html',
    }

    # Si el skin no está en el mapa, se usa 'default'
    template_path = template_map.get(cv.skin, 'cv_manager/skins/cv_default.html')

    return render(request, template_path, {'cv': cv})



# Vista pública para mostrar el CV según su skin
def cv_public_view(request, slug):
    cv = get_object_or_404(CVProfile, slug=slug)
    profile = UserProfile.objects.filter(user=cv.user).first()  # Obtener perfil del dueño del CV

    return render(request, f'cv_manager/skins/cv_{cv.skin}.html', {
        'cv': cv,
        'profile': profile,  # Pasamos profile para usar en la plantilla
    })



# Vista para listar todos los CVs del usuario autenticado
@login_required
def cv_list_view(request):
    cvs = CVProfile.objects.filter(user=request.user)
    return render(request, 'cv_manager/cv_list.html', {'cvs': cvs})


# ------------------------
# Descargas PDF / ZIP
# ------------------------


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
        'default': 'cv_manager/skins/pdf/cv_default_pdf.html',
        'modern': 'cv_manager/skins/pdf/cv_modern_pdf.html',
        'minimal': 'cv_manager/skins/pdf/cv_minimal_pdf.html',
    }
    template_path = template_map.get(cv.skin, 'cv_manager/skins/pdf/cv_default_pdf.html')

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
        # 🔹 Filtrar solo los CVs que pertenecen al usuario logueado
        cvs = CVProfile.objects.filter(id__in=selected_ids, user=request.user)

        if not cvs.exists():
            return HttpResponse("No se encontraron CVs propios para descargar.", status=403)

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
            'default': 'cv_manager/skins/pdf/cv_default_pdf.html',
            'modern': 'cv_manager/skins/pdf/cv_modern_pdf.html',
            'minimal': 'cv_manager/skins/pdf/cv_minimal_pdf.html',
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

# ------------------------
# ERROR 404 Y URL DESCONFIGURADA
# ------------------------

# vista error 404

def page_not_found_view(request, exception):
    return render(request, 'cv_manager/404.html', status=404)

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

    return render(request, 'cv_manager/info_url.html', contexto)
