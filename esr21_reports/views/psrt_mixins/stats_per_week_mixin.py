from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from datetime import datetime,timedelta
from django.db.models import Q
from edc_constants.constants import POS


class StatsPerWeekMixin(EdcBaseViewMixin):
    
    vaccination_model =  'esr21_subject.vaccinationdetails'
    pregnancy_model =  'esr21_subject.pregnancytest'
    
    @property
    def vaccination_model_cls(self):
        return django_apps.get_model(self.vaccination_model)
    
    @property
    def pregnancy_modell_cls(self):
        return django_apps.get_model(self.pregnancy_model)
    
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
                   # 'weekly_saes_stats',
                   # 'weekly_aesi_stats',
                   ]
    
        for filter in filters:
            cls_attrib = getattr(self, filter)
            filter_stats = []
            for week_date in self.weekly_dates:
                start_week_date =week_date[0]
                end_week_date = week_date[1]
                filter_stats.append(cls_attrib(start_week_date,end_week_date))
            weekly_stats[filter]=filter_stats
        return weekly_stats
        

    
    def weekly_enrollments_stats(self, start_week_date,end_week_date):
        stats = [f'{start_week_date} to {end_week_date}']
        overall_stats = self.count_overall_enrollments_stats_by_week(start_week_date, end_week_date)
        stats.append(overall_stats)
        for site_name in self.sites_names:
                site_stats = self.count_enrollment_stats_by_site(site_name, start_week_date, end_week_date)
                stats.append(site_stats)
        return stats
            
    
    def weekly_pregnancy_stats(self, start_week_date, end_week_date):
        stats = [f'{start_week_date} to {end_week_date}']
        overall_stats = self.count_overall_pregnancy_stats_by_week(start_week_date, end_week_date)
        stats.append(overall_stats)
        for site_name in self.sites_names:
                site_stats = self.count_pregnancy_stats_by_week(site_name, start_week_date, end_week_date)
                stats.append(site_stats)
        return stats
    
    def weekly_second_dose_stats(self, start_week_date, end_week_date):
        stats = [f'{start_week_date} to {end_week_date}']
        overall_stats = self.count_overall_second_dose_stats_by_week(start_week_date, end_week_date)
        stats.append(overall_stats)
        
        for site_name in self.sites_names:
                site_stats = self.count_second_dose_stats_by_week(site_name, start_week_date, end_week_date)
                stats.append(site_stats)
        return stats
            
    
    
    def weekly_aes_stats(self, start_week_date, end_week_date):
        stats = [f'{start_week_date} to {end_week_date}']
        overall_stats = self.count_overall_second_dose_stats_by_week(start_week_date, end_week_date)
        stats.append(overall_stats)
        
        for site_name in self.sites_names:
                site_stats = self.count_second_dose_stats_by_week(site_name, start_week_date, end_week_date)
                stats.append(site_stats)
        return stats
    
    def weekly_saes_stats(self,start_date, end_week_date):
        weekly_site_stats = []
        return weekly_site_stats
            
    
    
    def weekly_aesi_stats(self,start_week_date, end_week_date):
        weekly_site_stats = []
        return weekly_site_stats
    
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
    
    def count_pregnancy_stats_by_week(self, site_name_postfix, start_date, end_date):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            pregnancy = self.pregnancy_modell_cls.objects.filter(
                 Q(preg_date__lte=end_date) & Q(preg_date__gte=start_date)
                &Q(result=POS) & Q(site_id=site_id))
        return pregnancy.count()
    
    def count_overall_pregnancy_stats_by_week(self, start_date, end_date):
        pregnancy = self.pregnancy_modell_cls.objects.filter(
                Q(preg_date__lte=end_date) & Q(preg_date__gte=start_date)
                & Q(result=POS))
        return pregnancy.count()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            sites=self.sites_names,
            weekly_stats_by_filters=self.weekly_stats_by_filters,
        )
        return context
