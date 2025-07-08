from . import views
from django.urls import path

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('pregunta/<int:pk>/', views.pregunta_detail, name='pregunta_detail'),
    path('pregunta/create_private/', views.pregunta_create, name='pregunta_create_private'),
    path('pregunta/create_public/', views.pregunta_create_public, name='pregunta_create_public'),
    path('pregunta/<int:pk>/edit/', views.pregunta_edit, name='pregunta_edit'),
    path('pregunta/<int:pk>/delete/', views.pregunta_delete, name='pregunta_delete'),
    path('respuesta/create/<int:pk>/', views.respuesta_create, name='respuesta_create'),
    path('respuesta/<int:pk>/edit/', views.respuesta_edit, name='respuesta_edit'),
    path('respuesta/<int:pk>/delete/', views.respuesta_delete, name='respuesta_delete'),
]
