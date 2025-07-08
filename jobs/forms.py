from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobOffer, JobApplication
from .forms import JobOfferForm, JobApplicationForm


@login_required
def create_offer(request):
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
            return redirect('job_offer_list')
    else:
        form = JobOfferForm()
    
    return render(request, 'jobs/create_offer.html', {'form': form})


def job_offer_list(request):
    offers = JobOffer.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'jobs/job_offer_list.html', {'offers': offers})


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