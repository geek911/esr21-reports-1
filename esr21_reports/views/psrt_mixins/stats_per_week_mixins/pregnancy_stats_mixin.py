from django.apps import apps as django_apps
from edc_constants.constants import POS
from django.db.models import Q


class PregnancyStatsMixin:
    pregnancy_model =  'esr21_subject.pregnancytest'
    
    @property
    def pregnancy_model_cls(self):
        return django_apps.get_model(self.pregnancy_model)
    
    def weekly_pregnancy_stats(self, start_week_date, end_week_date):
        stats = [f'{start_week_date} to {end_week_date}']
        overall_stats = self.count_overall_pregnancy_stats_by_week(start_week_date, end_week_date)
        if overall_stats > 0:
            stats.append(overall_stats)
            for site_name in self.sites_names:
                    site_stats = self.count_pregnancy_stats_by_week(site_name, start_week_date, end_week_date)
                    stats.append(site_stats)
            return stats
        return None
    
    def count_pregnancy_stats_by_week(self, site_name_postfix, start_date, end_date):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            pregnancy = self.pregnancy_model_cls.objects.filter(
                 Q(preg_date__lte=end_date) & Q(preg_date__gte=start_date)
                &Q(result=POS) & Q(site_id=site_id))
        return pregnancy.count()
    
    def count_overall_pregnancy_stats_by_week(self, start_date, end_date):
        pregnancy = self.pregnancy_model_cls.objects.filter(
                Q(preg_date__lte=end_date) & Q(preg_date__gte=start_date)
                & Q(result=POS))
        return pregnancy.count()