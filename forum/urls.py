from . import views
from django.urls import path

urlpatterns = [
    path('forum/', views.forum_home, name='forum_home'),
    path('forum/pregunta/<int:pk>/', views.pregunta_detail, name='pregunta_detail'),
    path('forum/pregunta/create_private/', views.pregunta_create_private, name='pregunta_create_private'),
    path('forum/pregunta/create_public/', views.pregunta_create_public, name='pregunta_create_public'),
    path('forum/pregunta/<int:pk>/edit/', views.pregunta_edit, name='pregunta_edit'),
    path('forum/pregunta/<int:pk>/delete/', views.pregunta_delete, name='pregunta_delete'),
    path('forum/respuesta/create/<int:pk>/', views.respuesta_create, name='respuesta_create'),
    path('forum/respuesta/<int:pk>/edit/', views.respuesta_edit, name='respuesta_edit'),
    path('forum/respuesta/<int:pk>/delete/', views.respuesta_delete, name='respuesta_delete'),
]
