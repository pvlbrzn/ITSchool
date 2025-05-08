from django.apps import AppConfig


class ManagerPanelConfig(AppConfig):
    """
    Configuration class for the 'manager_panel' application.

    This class sets the default auto field for models and defines the app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manager_panel'
