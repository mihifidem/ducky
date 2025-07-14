from django import forms
from .models import JobOffer, JobApplication, User, Candidature


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