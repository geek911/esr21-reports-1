
from .summary_queries_mixins import (AdverseEventSummaryMixin,
                                     EnrollmentSummaryMixin,
                                     MedicalHistorySummaryMixin,
                                     VaccinationSummaryMixin,
                                     DemographicsSummaryMixin,
                                     PregnancySummaryMixin)

class SummaryQueriesMixin(AdverseEventSummaryMixin,
                          EnrollmentSummaryMixin,
                          MedicalHistorySummaryMixin,
                          VaccinationSummaryMixin,
                          PregnancySummaryMixin,
                          DemographicsSummaryMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            site_names = self.site_names,
        )

        return context
