from django.apps import apps as django_apps
from .adverse_event_mixin import AdverseEventRecordMixin


class AdverseEventRecordViewMixin(AdverseEventRecordMixin):
    ae_record_model = 'esr21_subject.adverseeventrecord'

    @property
    def ae_record_cls(self):
        return django_apps.get_model(self.ae_record_model)
