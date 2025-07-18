from django.urls import path
from . import views

urlpatterns = [
    path('', views.redireccion_dashboard, name='home'),
    path('dashboard/user/', views.dashboard_user, name='dashboard_user'),
    path('dashboard/premium/', views.dashboard_premium, name='dashboard_premium'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/teacher/', views.dashboard_teacher, name='dashboard_teacher'),
    path('dashboard/headhunter/', views.dashboard_headhunter, name='dashboard_headhunter'),
    path('dashboard/professional/', views.dashboard_profesional, name='dashboard_professional'),
    path('dashboard/', views.redireccion_dashboard, name='redireccion_dashboard'),
]
