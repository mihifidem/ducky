from django.urls import path
from . import views

urlpatterns = [
    path('ofertas/', views.job_offer_list, name='job_offer_list'),
    path('oferta/<int:offer_id>/', views.job_offer_detail, name='job_offer_detail'),
    path('oferta/<int:offer_id>/postular/', views.apply_to_offer, name='apply_to_offer'),
    path('crear/', views.create_offer, name='create_offer'),
    path('headhunter/', views.headhunter_dashboard, name='headhunter_dashboard'),
    path(
        'headhunter/oferta/<int:offer_id>/candidaturas/',
        views.offer_applications,
        name='offer_applications'
    ),
    path(
    'headhunter/candidature/<int:candidature_id>/update/',views.update_candidature_status,name='update_candidature_status'),
    path('headhunter/candidaturas/', views.candidature_list, name='candidature_list'),
    # Asegúrate de que la vista candidature_list exista
    path('mensaje/<int:offer_id>', views.message, name='message'),
    
]