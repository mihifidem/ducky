from django.urls import path
from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, signup_view, profile_view, edit_profile, delete_userprofile


urlpatterns = [
    
    # Authentication URLs
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),

     # Profile management
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='profile_edit'),
    path('profile/delete/', delete_userprofile, name='userprofile_delete_confirm'),

    
]



