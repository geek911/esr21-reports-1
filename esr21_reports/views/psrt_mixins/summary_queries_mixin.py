from curses.ascii import SI
import imp
from edc_base.view_mixins import EdcBaseViewMixin
from django.contrib.sites.models import Site
from django.apps import apps as django_apps
from django.db.models import Q

class SummaryQueriesMixin(EdcBaseViewMixin):

    """
    Data Anomalies in the EDC

    TODO:   Change method comments to descriptions to save as both
            comments as well as description
    """

    vaccination_details_model = 'esr21_subject.vaccinationdetails'
    eligibility_confirmation_model = 'esr21_subject.eligibilityconfirmation'
    medical_history_model = 'esr21_subject.medicalhistory'
    screening_eligibility_model = 'esr21_subject.screeningeligibility'
    informed_consent_model = 'esr21_subject.informedconsent'
    demographics_data_model = 'esr21_subject.demographicsdata'


    """
    CLS classes for the models being used from esr21-subject
    """
    
    @property
    def vaccination_details_cls(self):
        return django_apps.get_model(self.vaccination_details_model)

    @property
    def eligibility_confirmation_cls(self):
        return django_apps.get_model(self.eligibility_confirmation_model)

    @property
    def medical_history_cls(self):
        return django_apps.get_model(self.medical_history_model)

    @property
    def screening_eligibility_cls(self):
        return django_apps.get_model(self.screening_eligibility_model)

    @property
    def informed_consent_cls(self):
        return django_apps.get_model(self.informed_consent_model)

    @property
    def demographics_data_cls(self):
        return django_apps.get_model(self.demographics_data_model)

    

    """
    
    Queries of stuff being used in the DB

    """


    @property
    def site_ids(self):
        return Site.objects.order_by('id').values_list('id', flat=True)

    @property
    def site_names(self):
        site_names = Site.objects.order_by('id').values_list('name', flat=True)
        site_names = list(map(lambda name: name.split('-')[1], site_names))
        return site_names

    @property
    def enrolled(self):
        """
        Enrolled subject identifiers 

        NB: Received the first dose, that is the criteria
        """
        enrolled = self.vaccination_details_cls.objects.filter(received_dose_before='first_dose').values_list(
            'subject_visit__subject_identifier').distinct()
        return enrolled



    @property
    def ae_statistics(self):
        """
        AE start date is before first dose	
        """
        return ["AE start date is before first dose", 0, 0, 0, 0, 0, 0]

    @property
    def eligible_no_icf_statistics(self):
        """
        Eligible from eligibility confirmation but no ICF form	
        """

        screening_identifiers = self.eligibility_confirmation_cls.objects.values_list('screening_identifier').distinct()

        eligible_no_crfs = []

        for site_id in self.site_ids:
            no_consents = self.informed_consent_cls.objects.filter(Q(site_id=site_id) & ~Q(
                screening_identifier__in=screening_identifiers)).count()
            eligible_no_crfs.append(no_consents)

        return ["Eligible from eligibility confirmation but no ICF form", * eligible_no_crfs, sum(eligible_no_crfs)]

    @property
    def first_dose_second_dose_missing_statistics(self):
        """
        First dose missing and second dose not missing	
        """
        return ["First dose missing and second dose not missing", 0, 0, 0, 0, 0, 0]

    @property
    def male_child_bearing_potential_statistics(self):
        """
        Male and child bearing potential is Yes	
        """
        return ["First dose missing and second dose not missing", 0, 0, 0, 0, 0, 0]

    @property
    def no_hiv_results_statistics(self):
        """
        No HIV result	
        """
        return ["No HIV result", 0, 0, 0, 0, 0, 0]

    @property
    def no_medical_history_statistics(self):
        """
        No medical history form	
        """
        # enrolled with no medical histories
        no_medical_histories = []

        for site_id in self.site_ids:
            medical_histories = self.medical_history_cls.objects.filter(Q(site_id=site_id) & ~Q(
                subject_visit__subject_identifier__in=self.enrolled)).count()
            no_medical_histories.append(medical_histories)

        return ["No HIV result", *no_medical_histories, sum(no_medical_histories)]

    @property
    def no_preg_results_statistics(self):
        """
        No pregnancy result and F and child bearing potential	
        """
        return ["No pregnancy result and F and child bearing potential", 0, 0, 0, 0, 0, 0]

    @property
    def not_on_demograpics_statistics(self):
        """
        Not on demographic data	
        """
        # enrolled but no demographics
        no_demographics = []

        for site_id in self.site_ids:
            demographics = self.demographics_data_cls.objects.filter(
                ~Q(subject_visit__subject_identifier__in=self.enrolled) & Q(site=site_id)).count()

            no_demographics.append(demographics)

        return ["Not on demographic data", *no_demographics, sum(no_demographics)]

    @property
    def ineligible_vaccinated_participant_statistics(self):
        """
        participant vaccinated but ineligible	
        """

        # ineligible but vaccinated

        not_eligible = []

        ineligible_pids = self.screening_eligibility_cls.objects.filter(
            is_eligible=False).values_list('subject_identifier', flat=True)

        for site_id in self.site_ids:
            vaccinated_count = self.vaccination_details_cls.objects.filter(
                site_id=site_id, subject_visit__subject_identifier__in=ineligible_pids).count()
            not_eligible.append(vaccinated_count)

        return ["Participant vaccinated but ineligible", *not_eligible, sum(not_eligible)]

    @property
    def no_screening_for_icf_statistics(self):
        """
        Screening identifier found in informed consent but not in eligibility criteria	
        """

        # ineligible but fount in ICF
        ineligible_consents = []

        screening_identifiers = self.informed_consent_cls.objects.values_list(
            'screening_identifier', flat=True).distinct()

        for site_id in self.site_ids:
            consents = self.eligibility_confirmation_cls.objects.filter(Q(site_id=site_id) & Q(
                is_eligible=False) & Q(screening_identifier__in=screening_identifiers)).count()
            ineligible_consents.append(consents)
            
        return ["Screening identifier found in informed consent but not in eligibility criteria", *ineligible_consents, sum(ineligible_consents)]

    @property
    def vaccinated_no_icf_statistics(self):
        """
        subject_identifier is found in vaccination form but all of the following are missing: eligibility confirmation, informed consent and screening confirmation	
        """
        return ["subject_identifier is found in vaccination form but all of the following are missing: eligibility confirmation, informed consent and screening confirmation", 0, 0, 0, 0, 0, 0]


    """ 
    
    Context
    
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            ae_stats = self.ae_statistics,
            site_names = self.site_names,
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
