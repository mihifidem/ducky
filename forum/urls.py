from . import views
from django.urls import path

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('pregunta/<int:pk>/', views.PreguntaDetailView.as_view(), name='pregunta_detail'),
    path('ajax/cargar-profesionales/', views.cargar_profesionales, name='ajax_cargar_profesionales'),
    path('pregunta/create_private/', views.pregunta_create_private, name='pregunta_create_private'),
    path('pregunta/create_public/', views.pregunta_create_public, name='pregunta_create_public'),
    path('pregunta/<int:pk>/edit/', views.PreguntaUpadteView.as_view(), name='pregunta_edit'),
    path('pregunta/<int:pk>/delete/', views.PreguntaDeleteView.as_view(), name='pregunta_delete'),
    path('respuesta/create/<int:pk>/', views.respuesta_create, name='respuesta_create'),
    path('respuesta/<int:pk>/edit/', views.RespuestaUpadteView.as_view(), name='respuesta_edit'),
    path('respuesta/<int:pk>/delete/', views.RespuestaDeleteView.as_view(), name='respuesta_delete'),
    path('mail_list/', views.mail_list, name='mail_list'),
    path('mail_recibido/', views.mail_recibido, name='mail_recibido'),
]
