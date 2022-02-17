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
            demographics = self.demographics_data_cls.objects.filter(
                ~Q(subject_visit__subject_identifier__in=self.enrolled) &
                Q(site=site_id)).count()

            no_demographics.append(demographics)

        return ["Not on demographic data", *no_demographics, sum(no_demographics)]
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            no_demographics = self.not_on_demograpics_statistics)
        return context
    