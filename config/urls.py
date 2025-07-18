"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views  

urlpatterns = [
    # Ruta para el panel de administración de Django
    path("admin/", admin.site.urls),

    # URLs para la app 'account' (registro, login, etc.)
    path('account/', include('account.urls')),

    # Ruta principal que apunta a la vista home en core.views
    path('', core_views.home, name='home'),

    # Incluye las URLs por defecto de autenticación de Django (login, logout, password)
    path('account/', include('django.contrib.auth.urls')),

    # URLs de la app 'core' para dashboards y demás funcionalidades
    path('core/', include('core.urls')),
]

# Si estamos en modo DEBUG, servimos archivos media y static directamente desde el servidor de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
