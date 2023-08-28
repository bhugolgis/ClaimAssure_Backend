from django.apps import AppConfig


class ClaimmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ClaimManagement'


    def ready(self):
        import ClaimManagement.signals
