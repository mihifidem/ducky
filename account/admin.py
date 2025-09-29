from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'birthdate', 'phone']
    search_fields = ['user__username', 'role', 'phone']
    list_filter = ['role', 'birthdate']
    autocomplete_fields = ['user']

    # Solo admin puede eliminar
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # Staff puede ver pero no editar
    def has_change_permission(self, request, obj=None):
        if request.user.is_staff and not request.user.is_superuser:
            return False
        return True

