from django.db.models import Q
from django.apps import apps as django_apps


class EnrollmentStatsMixin:
    
    vaccination_model =  'esr21_subject.vaccinationdetails'
    
    @property
    def vaccination_model_cls(self):
        return django_apps.get_model(self.vaccination_model)
    
    def weekly_enrollments_stats(self, start_week_date,end_week_date):
        stats = [f'{start_week_date} to {end_week_date}']
        overall_stats = self.count_overall_enrollments_stats_by_week(start_week_date, end_week_date)
        if overall_stats > 0:
            stats.append(overall_stats)
            for site_name in self.sites_names:
                    site_stats = self.count_enrollment_stats_by_site(site_name, start_week_date, end_week_date)
                    stats.append(site_stats)
            return stats
        return None
    
    def count_enrollment_stats_by_site(self,site_name_postfix, start_date, end_date):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            vaccination = self.vaccination_model_cls.objects.filter(
                Q(vaccination_date__lte=end_date) & Q(vaccination_date__gte=start_date)
                & Q(site_id=site_id))
            return vaccination.count()
        return None
    
    def count_overall_enrollments_stats_by_week(self, start_date, end_date):
        vaccination = self.vaccination_model_cls.objects.filter(
                Q(vaccination_date__lte=end_date) & Q(vaccination_date__gte=start_date))
        return vaccination.count()
    
    @property
    def overall_enrollment_stats(self):
        overall_stats = []
        for week_date in self.weekly_dates:
            start_week_date =week_date[0]
            end_week_date = week_date[1]
            weekly_site_stats = self.weekly_enrollments_stats(start_week_date,end_week_date)
            if weekly_site_stats:
                overall_stats.append(weekly_site_stats)
                
        return overall_stats