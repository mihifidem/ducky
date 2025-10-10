"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views  # asumimos que home está en app "core"

from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from account.cv_manager.views import CVProfileViewSet

# Router DRF
router = DefaultRouter()
router.register(r'cvs', CVProfileViewSet, basename='cvs')

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="CV API",
        default_version='v1',
        description="API REST para gestionar los CVs del usuario",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,  # requiere autenticación
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('account/', include('account.urls')),
    path('account/cv/', include('account.cv_manager.urls')),
    path('', include('core.urls')),  # 👈 asegúrate de incluir tu app
# Página de inicio
    path('account/', include('django.contrib.auth.urls')),  # login/logout
    path('academy/', include('duckyAcademy.urls')),
    path('jobs/', include('jobs.urls')),  # URLs de la app jobs
    path('management_test/', include('management_test.urls')),

# APIs
    path('api/', include('account.cv_manager.urls')),  # nuestra API de CVs
    path('api-auth/', include('rest_framework.urls')),  # login/logout para SessionAuthentication
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

# Handlers de errores personalizados
handler404 = "account.cv_manager.views.cv_not_found_handler"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
