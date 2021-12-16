from django.views.generic.base import ContextMixin

from edc_constants.constants import YES


class VaccinationDataTablesViewMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        actual_aes_triggered = self.actual_aes_triggered()

        context.update(
            actual_aes_triggered=actual_aes_triggered)
        return context

    def actual_aes_triggered(self):
        vaccination_aes = self.vaccination_model_cls.objects.filter(
            adverse_event=YES).values_list('subject_visit_id')
        return self.ae_model_cls.objects.filter(subject_visit_id__in=vaccination_aes)
