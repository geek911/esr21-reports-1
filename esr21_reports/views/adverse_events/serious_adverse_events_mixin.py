
from edc_base.view_mixins import EdcBaseViewMixin
from .serious_adverse_event_mixin import SeriousAdverseEventRecordMixin


class SeriousAdverseEventRecordViewMixin(EdcBaseViewMixin,
                                         SeriousAdverseEventRecordMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            new_sae_listing=self.new_sae_listing,
            all_sae_records=self.all_sae_records,
            sae_overral_adverse_events=self.sae_overral_adverse_events,
            sae_hiv_uninfected=self.sae_hiv_uninfected,
            sae_hiv_infected=self.sae_hiv_infected,
            sae_received_first_dose=self.sae_received_first_dose,
            sae_received_second_dose=self.sae_received_second_dose,
            sae_related_ip=self.sae_related_ip,
            sae_not_related_ip=self.sae_not_related_ip,
            sae_received_first_dose_plus_28=self.sae_received_first_dose_plus_28
            )
        return context

