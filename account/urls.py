from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, profile_view
from .views import signup_view
<<<<<<< HEAD




urlpatterns = [
=======
from . import views


urlpatterns = [
    
    # Authentication URLs
>>>>>>> 7a09ebf (Sesion 1-2-3)
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('signup/', signup_view, name='signup'),
<<<<<<< HEAD

]
=======
    
    
    # Profile management URLs

    path('add-experience/', views.add_experience, name='add_experience'),
    path('add-education/', views.add_education, name='add_education'),
    path('add-language/', views.add_language, name='add_language'),
    path('add-softskill/', views.add_softskill, name='add_softskill'),
    path('add-hobby/', views.add_hobby, name='add_hobby'),
    path('crear-perfil/', views.create_profile_view, name='profile_create'),
    path('eliminar-perfil/', views.delete_userprofile, name='delete_userprofile_confirm'),
    
    # Dashboard and CV panel URLs
    path('cv-panel/', views.cv_panel_view, name='cv_panel'),
     path('dashboard/', views.dashboard_view, name='dashboard'),
     
     # User profile management URLs
    path('editar-perfil/', views.edit_profile, name='profile'),
    
    # Job experience management URLs
    path('experience/add/', views.add_experience, name='add_experience'),
    path('experience/edit/<int:pk>/', views.edit_experience, name='edit_experience'),
    path('experience/delete/<int:pk>/', views.delete_experience, name='delete_experience'),

]



>>>>>>> 7a09ebf (Sesion 1-2-3)
