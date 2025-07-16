from django import forms
from .models import JobOffer, JobApplication, User, Candidature, StatusMessageTemplate


class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = [
            'title',
            'company_name',
            'description',
            'location',
            'modality',
            'salary',
            'category',
            'requirements',
            'benefits',
            'is_active',
        ]


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['message']
        widgets = {
            'message': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Puedes incluir un mensaje opcional...'
                }
            )
        }

class CandidatureStatusForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['estado']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
class StatusMessageTemplateForm(forms.ModelForm):
    class Meta:
        model = StatusMessageTemplate
        fields = ['estado', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 5}),
        }