from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class ApplicationTokenConfig(AppConfig):
    name = 'application_token'

    def ready(self):
        autodiscover_modules('load')
