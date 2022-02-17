from django.apps import apps as django_apps
from django.db.models import Q
from edc_constants.constants import YES
from edc_base.view_mixins import EdcBaseViewMixin


class MedicalHistorySummaryMixin(EdcBaseViewMixin):
    medical_history_model = 'esr21_subject.medicalhistory'
    hiv_result_model = 'esr21_subject.rapidhivtesting'
    

    @property
    def medical_history_cls(self):
        return django_apps.get_model(self.medical_history_model)

    @property
    def rapid_hiv_cls(self):
        return django_apps.get_model(self.hiv_result_model)

    @property
    def male_child_bearing_potential_statistics(self):
        """
        Male and child bearing potential is Yes    
        """
        
        child_bearing_potential = []
        male_consents = self.consent_model_cls.objects.filter(
            gender='M').values_list('subject_identifier', flat=True)
        for site_id in self.site_ids:
            screening_eligibility = self.screening_eligibility_cls.objects.filter(
                Q(subject_identifier__in=male_consents) &
                Q(childbearing_potential=YES) &
                Q(site_id=site_id)).count()
            child_bearing_potential.append(screening_eligibility)
        return ['Male and child bearing potential is Yes', 
                *child_bearing_potential, sum(child_bearing_potential)]

    @property
    def no_hiv_results_statistics(self):
        """
        No HIV result    
        """
       
        hiv_results = []
        for site_id in self.site_ids:
            site_enrollment_pids = self.vaccination_details_cls.objects.filter(
                received_dose_before='first_dose',
                site_id=site_id).values_list(
            'subject_visit__subject_identifier',flat=True)
                
            existing_hiv_results = self.rapid_hiv_cls.objects.filter(Q(site_id=site_id) & Q(
                subject_visit__subject_identifier__in=site_enrollment_pids)).values_list(
                    'subject_visit__subject_identifier',flat=True)
                
            no_hiv_results = list(set(site_enrollment_pids) - set(existing_hiv_results))   
            hiv_results.append(len(no_hiv_results))
        
        return ['No HIV result', *hiv_results, sum(hiv_results)]

    @property
    def no_medical_history_statistics(self):
        """
        No medical history form    
        """

        no_medical_histories = []
        for site_id in self.site_ids:
            site_enrollment_pids = self.vaccination_details_cls.objects.filter(
                received_dose_before='first_dose',
                site_id=site_id).values_list(
            'subject_visit__subject_identifier',flat=True)

            medical_histories = self.medical_history_cls.objects.filter(Q(site_id=site_id) & Q(
                subject_visit__subject_identifier__in=site_enrollment_pids)).values_list(
                    'subject_visit__subject_identifier',flat=True)
 
            no_medical_history = list(set(site_enrollment_pids) - set(medical_histories))   
            no_medical_histories.append(len(no_medical_history))

        return ["No medical history form", *no_medical_histories, sum(no_medical_histories)]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            male_child_bearing_stats = self.male_child_bearing_potential_statistics,
            no_hiv_results_stats = self.no_hiv_results_statistics,
            no_medical_history_stats = self.no_medical_history_statistics,)

        return context