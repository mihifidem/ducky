from django.urls import path
from . import views

from .views import dashboard_view, cv_panel_view, mi_vista

urlpatterns = [
    # Dashboard / Panel
    path('dashboard/', dashboard_view, name='dashboard'),
    path('cv-panel/', cv_panel_view, name='cv_panel'),

    # Experiencia laboral (Job Experience)
    path('experience/', views.experience_list, name='experience_list'),
    path('experience/add/', views.add_experience, name='experience_add'),
    path('experience/<int:pk>/edit/', views.edit_experience, name='experience_edit'),
    path('experience/<int:pk>/delete/', views.delete_experience, name='experience_delete'),

    # Educación
    path('education/', views.education_list, name='education_list'),
    path('education/add/', views.add_education, name='education_add'),
    path('education/<int:pk>/edit/', views.edit_education, name='education_edit'),
    path('education/<int:pk>/delete/', views.delete_education, name='education_delete'),

    # Idiomas
    path('language/', views.language_list, name='language_list'),
    path('language/add/', views.add_language, name='language_add'),
    path('language/<int:pk>/edit/', views.edit_language, name='language_edit'),
    path('language/<int:pk>/delete/', views.delete_language, name='language_delete'),

    # Habilidades blandas (Soft Skills)
    path('softskill/', views.softskill_list, name='softskill_list'),
    path('softskill/add/', views.add_softskill, name='softskill_add'),
    path('softskill/<int:pk>/edit/', views.edit_softskill, name='softskill_edit'),
    path('softskill/<int:pk>/delete/', views.delete_softskill, name='softskill_delete'),

     # Hard Skill management URLs
    path('hardskill/', views.hardskill_list, name='hardskill_list'),
    path('hardskill/add/', views.add_hardskill, name='hardskill_add'),
    path('hardskill/edit/<int:pk>/', views.edit_hardskill, name='hardskill_edit'),
    path('hardskill/delete/<int:pk>/', views.delete_hardskill, name='hardskill_delete'),

    # Pasatiempos (Hobbies)
    path('hobby/', views.hobby_list, name='hobby_list'),
    path('hobby/add/', views.add_hobby, name='hobby_add'),
    path('hobby/<int:pk>/edit/', views.edit_hobby, name='hobby_edit'),
    path('hobby/<int:pk>/delete/', views.delete_hobby, name='hobby_delete'),

    # CRUD de CVs
    path('cv/', views.cv_list_view, name='cv_list'),
    path('cv/create/', views.cv_create, name='cv_create'),
    path('cv/<int:pk>/edit/', views.cv_edit, name='cv_edit'),
    path('cv/<int:pk>/delete/', views.cv_delete, name='cv_delete'),
    path('cv/<int:pk>/clone/', views.cv_clone, name='cv_clone'),

     # Vista pública y preview
    path('cv/<slug:slug>/preview/', views.preview_cv, name='cv_preview'),
    path('cv/<slug:slug>/view/', views.cv_public_view, name='cv_public_view'),

    # PDF export
    path('cv/<slug:slug>/download/', views.cv_download_pdf, name='cv_download'),
    path('cv/download-selected/', views.download_selected_cvs, name='cv_download_selected'),

    # 404
    path('*', views.page_not_found_view, name='error_404'),
    # URL 
    path('probar-url/', mi_vista, name='url_probar'),
]