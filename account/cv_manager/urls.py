from django.urls import path
from .views import   (
    cv_edit, cv_list, cv_create, cv_delete, cv_clone, 
dashboard_view, cv_panel_view, 
cv_public_view, cv_list_view, cv_download_pdf, mi_vista,
edit_experience, delete_experience, edit_education, delete_education, 
edit_language, delete_language, edit_softskill, delete_softskill, 
add_experience, add_education, add_language, add_softskill, add_hobby,
add_hardskill, edit_hardskill, delete_hardskill
)
from . import views

# Profile management URLs
urlpatterns = [
    path('add-experience/', views.add_experience, name='add_experience'),
    path('add-education/', views.add_education, name='add_education'),
    path('add-language/', views.add_language, name='add_language'),
    path('add-softskill/', views.add_softskill, name='add_softskill'),
    path('add-hardskill/', views.add_hardskill, name='add_hardskill'),
    path('add-hobby/', views.add_hobby, name='add_hobby'),
    
    
    # Education management URLs
    path('education/', views.education_list, name='education_list'),
    path('education/edit/<int:pk>/', views.edit_education, name='edit_education'),
    path('education/delete/<int:pk>/', views.delete_education, name='delete_education'),
  
    # lenguage management URLs
    path('languages/', views.language_list, name='language_list'),
    path('languages/edit/<int:pk>/', views.edit_language, name='edit_language'),
    path('languages/delete/<int:pk>/', views.delete_language, name='delete_language'),
    
    # Dashboard and CV panel URLs
    path('cv-panel/', views.cv_panel_view, name='cv_panel'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
             
    # Job experience management URLs
    path('experience/', views.experience_list, name='experience_list'),
    path('experience/edit/<int:pk>/', views.edit_experience, name='edit_experience'),
    path('experience/delete/<int:pk>/', views.delete_experience, name='delete_experience'),
    
    # Soft skill management URLs
    path('softskills/', views.softskill_list, name='softskill_list'),
    path('softskills/edit/<int:pk>/', views.edit_softskill, name='edit_softskill'),
    path('softskills/delete/<int:pk>/', views.delete_softskill, name='delete_softskill'),

    # Hard Skill management URLs
    path('hardskills/', views.hardskill_list, name='hardskill_list'),
    path('hardskills/edit/<int:pk>/', views.edit_hardskill, name='edit_hardskill'),
    path('hardskills/delete/<int:pk>/', views.delete_hardskill, name='delete_hardskill'),
    
    # Hobby management URLs
    path('hobbies/', views.hobby_list, name='hobby_list'),
    path('hobbies/edit/<int:pk>/', views.edit_hobby, name='edit_hobby'),
    path('hobbies/delete/<int:pk>/', views.delete_hobby, name='delete_hobby'),
    
    # CV Profile management URLs
    path('cvs/', cv_list_view, name='cv_list'),
    path('cvs/create/', cv_create, name='cv_create'),
    path('cvs/<slug:slug>/preview/', views.preview_cv, name='cv_preview'),
    path('cvs/<int:pk>/edit/', cv_edit, name='cv_edit'),
    path('cvs/<int:pk>/delete/', cv_delete, name='cv_delete'),
    path('cvs/<int:pk>/clone/', cv_clone, name='cv_clone'),
        
    
    # PDF generation URL
    path('cvs/<slug:slug>/download/', cv_download_pdf,name='download_cv_pdf'),
    # Public CV view URL
    path('cv/<slug:slug>/', cv_public_view, name='cv_public_view'),
    path('descargar-cvs/', views.download_selected_cvs, name='download_selected_cvs'),
    # 404
    path('*', views.page_not_found_view, name='error_404'),
    # URL 
    path('probar-url/', mi_vista, name='probar_url'),
]