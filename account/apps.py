from django.apps import AppConfig

<<<<<<< HEAD

class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"
=======
class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        import account.signals
>>>>>>> 7a09ebf (Sesion 1-2-3)
