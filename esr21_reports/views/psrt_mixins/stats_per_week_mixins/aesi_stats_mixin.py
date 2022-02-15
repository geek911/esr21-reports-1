from django.apps import apps as django_apps


class AESpecialInterestStatsMixin:
    
    aesi_model = 'esr21_subject.specialinterestadverseeventrecord'

    
    @property
    def aesi_model_cls(self):
        return django_apps.get_model(self.aesi_model)
    
    def weekly_aesi_stats(self,start_week_date, end_week_date):
        stats = [f'{start_week_date} to {end_week_date}']
        overall_stats = self.count_overall_aesi_stats_by_week(start_week_date, end_week_date)
        if overall_stats > 0:
            stats.append(overall_stats)
            for site_name in self.sites_names:
                    site_stats = self.count_aesi_stats_by_week(site_name, start_week_date, end_week_date)
                    stats.append(site_stats)
            return stats
        return None
    
    
    def count_aesi_stats_by_week(self, site_name_postfix, start_date, end_date):
        model_cls = 'aesi_model_cls'
        return self.count_stats_by_week(model_cls, site_name_postfix, start_date, end_date)
    
    def count_overall_aesi_stats_by_week(self, start_date, end_date):
        model_cls = 'aesi_model_cls'
        return self.count_overall_stats_by_week(model_cls, start_date, end_date)