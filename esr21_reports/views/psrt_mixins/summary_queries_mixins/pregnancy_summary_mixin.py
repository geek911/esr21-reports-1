from edc_base.view_mixins import EdcBaseViewMixin
from django.db.models import Q
from edc_constants.constants import YES

from django.apps import apps as django_apps


class PregnancySummaryMixin(EdcBaseViewMixin):
    
    pregnancy_test_model = 'esr21_subject.pregnancytest'
    
    @property
    def pregnancy_test_model_cls(self):
        return django_apps.get_model(self.pregnancy_test_model)
    
    @property
    def no_preg_results_statistics(self):
        """
        No pregnancy result and F and child bearing potential    
        """
        
        no_pregnancy_test = []
        female_consents = self.consent_model_cls.objects.filter(
            gender='F').values_list('subject_identifier', flat=True)
        for site_id in self.site_ids:
            screening_eligibility = self.screening_eligibility_cls.objects.filter(
                Q(subject_identifier__in=female_consents) &
                Q(childbearing_potential=YES) &
                Q(site_id=site_id)).values_list('subject_identifier', flat=True)
                
            pregnancy = self.pregnancy_test_model_cls.objects.filter(
                Q(subject_visit__subject_identifier__in=screening_eligibility) &
                Q(site_id=site_id)
                ).values_list('subject_visit__subject_identifier', flat=True)
                
                
            no_pregnancy = list(set(screening_eligibility) - set(pregnancy))
                
            
            no_pregnancy_test.append(len(no_pregnancy))
            
    
        return ['No pregnancy result and F and child bearing potential', 
                *no_pregnancy_test, sum(no_pregnancy_test)]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            no_preg_results_stats = self.no_preg_results_statistics,
        )

        return context
        