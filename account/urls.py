from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, profile_view, cv_edit, cv_list, cv_create, cv_delete, cv_clone, signup_view, dashboard_view, cv_panel_view, edit_profile, delete_userprofile, cv_public_view, cv_list_view, cv_download_pdf, mi_vista
from . import views


urlpatterns = [
    
    # Authentication URLs
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('signup/', signup_view, name='signup'),
    
    
    # Profile management URLs

    path('add-experience/', views.add_experience, name='add_experience'),
    path('add-education/', views.add_education, name='add_education'),
    path('add-language/', views.add_language, name='add_language'),
    path('add-softskill/', views.add_softskill, name='add_softskill'),
    path('add-hobby/', views.add_hobby, name='add_hobby'),
    path('crear-perfil/', views.create_profile_view, name='profile_create'),
    path('eliminar-perfil/', views.delete_userprofile, name='delete_userprofile_confirm'),
    
    # Education management URLs
    path('education/edit/<int:pk>/', views.edit_education, name='edit_education'),
    path('education/delete/<int:pk>/', views.delete_education, name='delete_education'),
  
    # lenguage management URLs
    path('languages/edit/<int:pk>/', views.edit_language, name='edit_language'),
    path('languages/delete/<int:pk>/', views.delete_language, name='delete_language'),
    
    # Dashboard and CV panel URLs
    path('cv-panel/', views.cv_panel_view, name='cv_panel'),
     path('dashboard/', views.dashboard_view, name='dashboard'),
     
     # User profile management URLs
    path('editar-perfil/', views.edit_profile, name='profile'),
    
    # Job experience management URLs
    path('experience/edit/<int:pk>/', views.edit_experience, name='edit_experience'),
    path('experience/delete/<int:pk>/', views.delete_experience, name='delete_experience'),
    
    # Soft skill management URLs
    path('softskills/edit/<int:pk>/', views.edit_softskill, name='edit_softskill'),
    path('softskills/delete/<int:pk>/', views.delete_softskill, name='delete_softskill'),
    
    # Hobby management URLs
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



