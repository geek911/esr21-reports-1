from django.apps import apps as django_apps
from django.views.generic.base import ContextMixin


class MissingCrfsMixin(ContextMixin):

    registered_subject_cls = django_apps.get_model('edc_registration.registeredsubject')
    crfmetadata_cls = django_apps.get_model('edc_metadata.crfmetadata')

    def missing_crfs(self, start_date=None, end_date=None):
        registered_identifiers = []
        if start_date and end_date:
            registered_identifiers = self.registered_subject_cls.objects.filter(
                created__gte=start_date,
                created__lte=end_date).values_list(
                    'subject_identifier', flat=True)
        else:
            registered_identifiers = self.registered_subject_cls.objects.all().values_list(
                'subject_identifier', flat=True)
        required_crfs = self.crfmetadata_cls.objects.filter(
            subject_identifier__in=registered_identifiers, entry_status='REQUIRED')

        return required_crfs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        missing_crfs = self.missing_crfs()
        context.update(
            missing_crfs=missing_crfs)
        return context
