from django.views.generic.base import ContextMixin

from edc_constants.constants import YES, NO


class VaccinationDataTablesViewMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        actual_aes_triggered = self.actual_aes_triggered()
        missing_aes_triggered = self.missing_aes_triggered()
        unexpected_aes = self.unexpected_aes()

        context.update(
            actual_aes_triggered=actual_aes_triggered,
            missing_aes_triggered=missing_aes_triggered,
            unexpected_aes=unexpected_aes)
        return context

    def actual_aes_triggered(self):
        vaccination_aes = self.vaccination_model_cls.objects.filter(
            adverse_event=YES).values_list('subject_visit_id')
        return self.ae_model_cls.objects.filter(subject_visit_id__in=vaccination_aes)

    def missing_aes_triggered(self):
        vaccination_aes = self.vaccination_model_cls.objects.filter(
            adverse_event=YES)
        actual_aes = self.actual_aes_triggered()
        return vaccination_aes.exclude(
            subject_visit_id__in=actual_aes.values_list('subject_visit_id', flat=True))

    def unexpected_aes(self):
        vaccination_aes = self.vaccination_model_cls.objects.filter(
            adverse_event=NO).values_list('subject_visit_id')
        return self.ae_model_cls.objects.filter(subject_visit_id__in=vaccination_aes)
