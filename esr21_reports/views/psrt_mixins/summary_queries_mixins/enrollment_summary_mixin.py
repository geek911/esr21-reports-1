from django.apps import apps as django_apps
from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin


class EnrollmentSummaryMixin(EdcBaseViewMixin):
    
    eligibility_confirmation_model = 'esr21_subject.eligibilityconfirmation'
    informed_consent_model = 'esr21_subject.informedconsent'
    screening_eligibility_model = 'esr21_subject.screeningeligibility'
    
    @property
    def eligibility_confirmation_cls(self):
        return django_apps.get_model(self.eligibility_confirmation_model)
    
    @property
    def screening_eligibility_cls(self):
        return django_apps.get_model(self.screening_eligibility_model)

    
    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.informed_consent_model)
    
    @property
    def enrolled(self):
        """
        Enrolled subject identifiers 

        NB: Received the first dose, that is the criteria
        """
        enrolled = self.vaccination_details_cls.objects.filter(received_dose_before='first_dose').values_list(
            'subject_visit__subject_identifier',flat=True).distinct()
        return enrolled


    @property
    def eligible_no_icf_statistics(self):
        """
        Eligible from eligibility confirmation but no ICF form    
        """
        no_consent_screenigs = []
        
        for site_id in self.site_ids:
            eligible_identifier = self.eligibility_model_cls.objects.filter(
                is_eligible=True, site_id=site_id).values_list('screening_identifier', flat=True)
            eligible_identifier = list(set(eligible_identifier))
            consent_screening_ids = self.consent_model_cls.objects.filter(site_id=site_id).values_list('screening_identifier', flat=True)
            consent_screening_ids = list(set(consent_screening_ids))
            no_consent_screenigs.append(len(list(set(eligible_identifier) - set(consent_screening_ids))))

        return ["Eligible from eligibility confirmation but no ICF form", *no_consent_screenigs, sum(no_consent_screenigs)]

    @property
    def no_screening_for_icf_statistics(self):
        """
        Screening identifier found in informed consent but not in eligibility criteria    
        """

        ineligible_consents = []

        screening_identifiers = self.consent_model_cls.objects.values_list(
            'screening_identifier', flat=True).distinct()

        for site_id in self.site_ids:
            consents = self.eligibility_confirmation_cls.objects.filter(Q(site_id=site_id) & Q(
                is_eligible=False) & Q(screening_identifier__in=screening_identifiers)).count()
            ineligible_consents.append(consents)
            
        return ["Screening identifier found in informed consent but not in eligibility criteria", *ineligible_consents, sum(ineligible_consents)]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            eligible_no_icf_stats = self.eligible_no_icf_statistics,
            ineligible_vaccinated_participants_stats = self.ineligible_vaccinated_participant_statistics,
            no_screening_for_icf_stats = self.no_screening_for_icf_statistics,
        )

        return context