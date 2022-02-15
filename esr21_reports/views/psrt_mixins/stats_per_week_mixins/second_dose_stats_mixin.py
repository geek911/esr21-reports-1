from django.db.models import Q


class SecondDoseStatsMixins:
    
    def weekly_second_dose_stats(self, start_week_date, end_week_date):
        stats = [f'{start_week_date} to {end_week_date}']
        overall_stats = self.count_overall_second_dose_stats_by_week(start_week_date, end_week_date)
        if overall_stats > 0:
            stats.append(overall_stats)
            for site_name in self.sites_names:
                    site_stats = self.count_second_dose_stats_by_week(site_name, start_week_date, end_week_date)
                    stats.append(site_stats)
            return stats
        return None
        
    def count_second_dose_stats_by_week(self, site_name_postfix, start_date, end_date):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            vaccination = self.vaccination_model_cls.objects.filter(
                    Q(vaccination_date__lte=end_date) & Q(vaccination_date__gte=start_date)
                    & Q(received_dose_before='second_dose') & Q(site_id=site_id))
        return vaccination.count()
    
    def count_overall_second_dose_stats_by_week(self, start_date, end_date):
        vaccination = self.vaccination_model_cls.objects.filter(
                Q(vaccination_date__lte=end_date) & Q(vaccination_date__gte=start_date)
                & Q(received_dose_before='second_dose'))
        return vaccination.count()