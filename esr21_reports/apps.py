from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'esr21_reports'
    verbose_name = 'ESR21 Reports'
    admin_site_name = 'esr21_reports_admin'
    extra_assignee_choices = ()
    assignable_users_group = 'assignable users'

    def ready(self):
        pass
