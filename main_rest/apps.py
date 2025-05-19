from django.apps import AppConfig


class MainRestConfig(AppConfig):
    """
    Configuration class for the 'main_rest' application.
    Sets the default auto field and application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_rest'
