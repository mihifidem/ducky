from django.urls import path
from . import views
from .views import CandidaturaDetailView # T42 añadimos la URL para la vista en detalle

urlpatterns = [
    # --- URLs públicas (candidatos y headhunters) ---
    path('ofertas/', views.JobOfferList.as_view(), name='job_offer_list'),  
    path('oferta/<int:offer_id>/', views.JobOfferDetailView.as_view(), name='job_offer_detail'), 
    path('oferta/<int:offer_id>/postular/', views.apply_to_offer, name='apply_to_offer'),  

    # --- Creación y edición de ofertas (solo headhunters) ---
    path('headhunter/oferta/crear/', views.CreateOfferView.as_view(), name='create_offer'), 
    path('headhunter/oferta/<int:offer_id>/editar/', views.EditOfferView.as_view(), name='edit_offer'),  

    # --- Dashboards ---
    path('headhunter/dashboard/', views.HeadhunterDashboardView.as_view(), name='headhunter_dashboard'), 
    path('candidato/', views.candidate_dashboard, name='candidate_dashboard'), 
    path('home/', views.HomeView.as_view(), name='home_job'), 
    path('headhunter/oferta/<int:offer_id>/candidaturas/', views.OfferApplicationsView.as_view(), name='offer_applications'),


    # --- Gestión de candidaturas (solo headhunters) ---
    path('headhunter/oferta/<int:offer_id>/candidaturas/', views.OfferApplicationsView.as_view(), name='offer_applications'),  
    path('headhunter/candidatura/<int:candidature_id>/cambiar-estado/', views.cambiar_estado_candidatura, name='cambiar_estado_candidatura'),
    path("candidaturas/<int:pk>/", CandidaturaDetailView.as_view(), name="candidatura_detail"),
    

    # Retirar candidatura (solo candidatos)
    path('candidato/candidatura/<int:candidature_id>/retirar/', views.withdraw_application, name='withdraw_application'),


    # --- Agenda del headhunter ---
    path('headhunter/agenda/', views.agenda, name='agenda'),
    path('headhunter/api/acciones/', views.api_acciones_headhunter, name='api_acciones_headhunter'),
    path('headhunter/crear-accion-ajax/', views.crear_accion_ajax, name='crear_accion_ajax'),
    path('headhunter/agenda/editar-accion-ajax/<int:accion_id>/', views.editar_accion_ajax, name='editar_accion_ajax'),
    path('headhunter/agenda/eliminar-accion-ajax/<int:accion_id>/', views.eliminar_accion_ajax, name='eliminar_accion_ajax'),
]
