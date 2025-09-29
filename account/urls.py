from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, profile_view, signup_view, edit_profile, delete_userprofile, create_profile_view
from . import views


urlpatterns = [
    
    # Authentication URLs
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),

    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/delete/', delete_userprofile, name='delete_userprofile_confirm'),
    path('profile/create/', views.create_profile_view, name='create_profile'),
    
]



