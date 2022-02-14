import imp
from edc_base.view_mixins import EdcBaseViewMixin
from django.contrib.sites.models import Site

class SummaryQueriesMixin(EdcBaseViewMixin):

    """
    Data Anomalies in the EDC
    """

    @property
    def site_ids(self):
        return Site.objects.order_by('id').values_list('id', flat=True)

    @property
    def ae_statistics(self):
        """
        AE start date is before first dose	
        """
        return [0,0,0,0,0, 0]

    @property
    def eligible_no_icf_statistics(self):
        """
        Eligible from eligibility confirmation but no ICF form	
        """
        return [0, 0, 0, 0, 0, 0]

    @property
    def first_dose_second_dose_missing_statistics(self):
        """
        First dose missing and second dose not missing	
        """
        return [0, 0, 0, 0, 0, 0]

    @property
    def male_child_bearing_potential_statistics(self):
        """
        Male and child bearing potential is Yes	
        """
        return [0, 0, 0, 0, 0, 0]

    @property
    def no_hiv_results_statistics(self):
        """
        No HIV result	
        """
        return [0, 0, 0, 0, 0, 0]

    @property
    def no_medical_history_statistics(self):
        """
        No medical history form	
        """
        return [0, 0, 0, 0, 0, 0]

    @property
    def no_preg_results_statistics(self):
        """
        No pregnancy result and F and child bearing potential	
        """
        return [0, 0, 0, 0, 0, 0]

    @property
    def not_on_demograpics_statistics(self):
        """
        Not on demographic data	
        """
        return [0, 0, 0, 0, 0, 0]

    @property
    def ineligible_vaccinated_participant_statistics(self):
        """
        participant vaccinated but ineligible	
        """
        return [0, 0, 0, 0, 0, 0]

    @property
    def no_screening_for_icf_statistics(self):
        """
        Screening identifier found in informed consent but not in eligibility criteria	
        """
        return [0, 0, 0, 0, 0, 0]

    @property
    def vaccinated_no_icf_statistics(self):
        """
        subject_identifier is found in vaccination form but all of the following are missing: eligibility confirmation, informed consent and screening confirmation	
        """
        return [0, 0, 0, 0, 0, 0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            ae_stats = self.ae_statistics,
            eligible_no_icf_stats = self.eligible_no_icf_statistics,
            first_dose_second_dose_stats = self.first_dose_second_dose_missing_statistics,
            ineligible_vaccinated_participants_stats = self.ineligible_vaccinated_participant_statistics,
            male_child_bearing_stats = self.male_child_bearing_potential_statistics,
            no_hiv_results_stats = self.no_hiv_results_statistics,
            no_medical_history_stats = self.no_medical_history_statistics,
            no_preg_results_stats = self.no_preg_results_statistics,
            no_screening_for_icf_stats = self.no_screening_for_icf_statistics,
            no_demographics = self.not_on_demograpics_statistics,
            vaccinated_no_icf_stats = self.vaccinated_no_icf_statistics
        )

        return context
