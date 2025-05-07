from django.apps import AppConfig


class MainConfig(AppConfig):
    """
    Configuration class for the 'main' application.

    Sets the default primary key type to BigAutoField and registers the app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
