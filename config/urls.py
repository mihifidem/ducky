from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('account/', include('account.urls')),
    path('', core_views.home, name='home'),
    path('account/', include('django.contrib.auth.urls')),
    path('core/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
