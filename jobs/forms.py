from django import forms
from .models import JobOffer, JobApplication


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
            'is_active'
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