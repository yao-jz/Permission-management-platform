from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class UserRoleRelationConfig(AppConfig):
    name = 'user_role_relation'

    def ready(self) -> None:
        autodiscover_modules('load')
