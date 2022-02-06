from django.apps import apps as django_apps
from .adverse_event_mixin import AdverseEventRecordMixin


class SeriousAdverseEventRecordViewMixin(AdverseEventRecordMixin):

    sae_record_model = 'esr21_subject.seriousadverseeventrecord'

    @property
    def sae_record_cls(self):
        return django_apps.get_model(self.sae_record_model)

