from django.urls import path
from . import views

urlpatterns = [
    path('ofertas/', views.job_offer_list, name='job_offer_list'),
    path('oferta/<int:pk>/', views.job_offer_detail, name='job_offer_detail'),
    path('oferta/<int:pk>/postular/', views.apply_to_offer, name='apply_to_offer'),
    path('crear/', views.create_offer, name='create_offer'),
]