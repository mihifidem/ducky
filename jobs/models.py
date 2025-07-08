from django.db import models
from django.contrib.auth.models import User

# Oferta de empleo creada por un headhunter
class JobOffer(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_offers')
    company_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    modality = models.CharField(
        max_length=20,
        choices=[
            ('remote', 'Remote'),
            ('onsite', 'On Site'),
            ('hybrid', 'Hybrid')
        ],
        default='onsite'
    )
    salary = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"

# Candidatura de un usuario a una oferta
class JobApplication(models.Model):
    offer = models.ForeignKey(
        JobOffer,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)

    class Meta:
        unique_together = ('offer', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} → {self.offer.title}"

