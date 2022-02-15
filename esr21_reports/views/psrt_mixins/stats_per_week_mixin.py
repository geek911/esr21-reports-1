from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from datetime import datetime,timedelta
from django.db.models import Q
from .stats_per_week_mixins import (EnrollmentStatsMixin,
                                    PregnancyStatsMixin,
                                    SecondDoseStatsMixins,
                                    SeriousAdverseEventStatsMixin,
                                    AdverseEventStatsMixin)


class StatsPerWeekMixin(EnrollmentStatsMixin,
                        PregnancyStatsMixin,
                        AdverseEventStatsMixin,
                        SecondDoseStatsMixins,
                        SeriousAdverseEventStatsMixin,
                        EdcBaseViewMixin):
    @property
    def weekly_dates(self):
        vaccination = self.vaccination_model_cls.objects.filter(
            received_dose_before='first_dose').earliest('created')
        vaccination_date = vaccination.vaccination_date
        
        study_close_datetime = datetime.now().date()
            
        study_open_datetime = vaccination_date.date()        
        
        week_pair_dates = []
        while study_open_datetime != study_close_datetime:
            study_open_datetime += timedelta(days=1)
            if study_open_datetime.weekday() == 6:
                start_week = study_open_datetime - timedelta(days=6)
                end_week = study_open_datetime
                week_pair_dates.append((start_week,end_week))      
        return week_pair_dates
    
    @property
    def weekly_stats_by_filters(self):
        weekly_stats = {}
        filters = ['weekly_enrollments_stats',
                   'weekly_pregnancy_stats',
                   'weekly_second_dose_stats',
                   'weekly_aes_stats',
                   'weekly_saes_stats',
                   'weekly_aesi_stats',
                   ]
    
        for filter in filters:
            cls_attrib = getattr(self, filter)
            filter_stats = []
            for week_date in self.weekly_dates:
                start_week_date =week_date[0]
                end_week_date = week_date[1]
                weekly_site_stats = cls_attrib(start_week_date,end_week_date)
                if weekly_site_stats:
                    filter_stats.append(weekly_site_stats)
                    
            if len(filter_stats) > 0:
                weekly_stats[filter]=filter_stats
        return weekly_stats
    
    
    def count_stats_by_week(self, model_cls, site_name_postfix, start_date, end_date):
        model_cls = getattr(self, model_cls)
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            aes = model_cls.objects.filter(
                 Q(start_date__lte=end_date) & Q(start_date__gte=start_date)
                 & Q(site_id=site_id))
        return aes.count()
    
    def count_overall_stats_by_week(self, model_cls, start_date, end_date):
        model_cls = getattr(self, model_cls)
        overall = model_cls.objects.filter(
                Q(start_date__lte=end_date) & Q(start_date__gte=start_date))
        return overall.count()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            sites=self.sites_names,
            weekly_stats_by_filters=self.weekly_stats_by_filters,
        )
        return context
