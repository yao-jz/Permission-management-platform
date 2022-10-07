from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class VerifyCodeConfig(AppConfig):
    name = 'verify_code'

    def ready(self):
        autodiscover_modules('load')
