from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import JobOffer, JobApplication, Candidature
from .forms import JobOfferForm, JobApplicationForm, CandidatureStatusForm
from django.contrib import messages


def create_offer(request): # Agrege el metodo POST porque estaba en GET y no se guardaba la oferta
    if not request.user.groups.filter(name='headhunter').exists():
        messages.error(request, "Solo los headhunters pueden crear ofertas.")
        return redirect('home')

    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.created_by = request.user
            offer.save()
            messages.success(request, "Oferta creada correctamente.")
            return redirect('job_offer_list')  # Cambia esto si tu URL se llama diferente
    else:
        form = JobOfferForm()

    return render(request, 'jobs/create_offer.html', {'form': form})

from django.shortcuts import render
from .models import JobOffer # Asume que tienes un modelo JobOffer
# Importa el modelo User si necesitas acceder a él directamente, aunque request.user ya lo proporciona
# from django.contrib.auth.models import User 

def job_offer_list(request):

    offers = JobOffer.objects.filter(is_active=True).order_by('-created_at')
    offers = JobOffer.objects.all()

    # Comprobamos si el usuario es headhunter
    is_headhunter = request.user.groups.filter(name='headhunter').exists()

    return render(request, 'jobs/job_offer_list.html', {
        'offers': offers,
        'is_headhunter': is_headhunter,
    })
   
    

    offers = JobOffer.objects.all() # O tu lógica para obtener las ofertas

#     # Agrega esta lógica para verificar si el usuario es un headhunter
#     is_headhunter = False
#     if request.user.is_authenticated:
#         is_headhunter = request.user.groups.filter(name='headhunter').exists()

    context = {
        'offers': offers,
        'is_headhunter': is_headhunter, # Pasa esta variable al contexto
    }
    return render(request, 'jobs/job_offer_list.html', context)
# def job_offer_list(request):
#     offers = JobOffer.objects.filter(is_active=True).order_by('-created_at')
#     return render(request, 'jobs/job_offer_list.html', {'offers': offers})



def job_offer_detail(request, pk):
    offer = get_object_or_404(JobOffer, pk=pk)
    return render(request, 'jobs/job_offer_detail.html', {'offer': offer})


@login_required
def apply_to_offer(request, pk):
    offer = get_object_or_404(JobOffer, pk=pk)

    if JobApplication.objects.filter(offer=offer, applicant=request.user).exists():
        messages.warning(request, "Ya te has postulado a esta oferta.")
        return redirect('job_offer_detail', pk=pk)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.offer = offer
            application.applicant = request.user
            application.save()
            messages.success(request, "Postulación enviada con éxito.")
            return redirect('job_offer_list')
    else:
        form = JobApplicationForm()

    return render(request, 'jobs/apply_to_offer.html', {'form': form, 'offer': offer})

@login_required
def headhunter_dashboard(request):
    if not request.user.groups.filter(name='headhunter').exists():
        messages.error(request, "Acceso restringido al rol headhunter.")
        return redirect('home')

    offers = JobOffer.objects.filter(created_by=request.user)
    return render(request, 'jobs/headhunter_dashboard.html', {
        'offers': offers
    })

@login_required
def offer_applications(request, offer_id):
    offer = get_object_or_404(JobOffer, id=offer_id, created_by=request.user)
    applications = offer.applications.all()
    return render(request, 'jobs/offer_applications.html', {
        'offer': offer,
        'applications': applications
    })

@login_required
def update_candidature_status(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)

    if request.method == 'POST':
        form = CandidatureStatusForm(request.POST, instance=candidature)
        if form.is_valid():
            form.save()
            return redirect('headhunter_dashboard')  # o la ruta deseada
    else:
        form = CandidatureStatusForm(instance=candidature)

    return render(request, 'joboffers/update_candidature_status.html', {
        'form': form,
        'candidature': candidature
    })