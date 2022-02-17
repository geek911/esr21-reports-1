from django.apps import apps as django_apps
from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin

class DemographicsSummaryMixin(EdcBaseViewMixin):
    
    demographics_data_model = 'esr21_subject.demographicsdata'
    
    @property
    def demographics_data_cls(self):
        return django_apps.get_model(self.demographics_data_model)
    
    @property
    def not_on_demograpics_statistics(self):
        """
        Not on demographic data    
        """
        
        
        
        
        # enrolled but no demographics
        no_demographics = []

        for site_id in self.site_ids:
            
            site_enrollment_pids = self.vaccination_details_cls.objects.filter(
                received_dose_before='first_dose',
                site_id=site_id).values_list(
            'subject_visit__subject_identifier',flat=True)
            
            
            demographics_pids = self.demographics_data_cls.objects.filter(
                Q(subject_visit__subject_identifier__in=site_enrollment_pids) &
                Q(site=site_id)).values_list(
            'subject_visit__subject_identifier',flat=True)
                
            no_demographics_data = list(set(site_enrollment_pids) - set(demographics_pids))

            no_demographics.append(len(no_demographics_data))

        return ["Not on demographic data", *no_demographics, sum(no_demographics)]
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            no_demographics = self.not_on_demograpics_statistics)
        return context
    