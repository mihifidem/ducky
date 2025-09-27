# mi_app/decorators.py

from django.http import HttpResponseForbidden
from functools import wraps

def role_required(allowed_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if hasattr(request.user, 'role') and request.user.role == allowed_role:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("No tienes permiso para acceder.")
            else:
                return HttpResponseForbidden("Debes iniciar sesión.")
        return _wrapped_view
    return decorator
