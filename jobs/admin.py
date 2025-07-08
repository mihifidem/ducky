
from django.contrib import admin
from .models import JobOffer, JobApplication

@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'created_by', 'is_active', 'created_at']
    list_filter = ['is_active', 'modality']
    search_fields = ['title', 'company_name', 'created_by__username']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['offer', 'applicant', 'applied_at']
    search_fields = ['offer__title', 'applicant__username']


