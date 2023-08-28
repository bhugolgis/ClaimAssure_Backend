from django.apps import AppConfig


class QueryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Query'

    def ready(self):
        import Query.signals
        # from Query import schedular
        # schedular.start()