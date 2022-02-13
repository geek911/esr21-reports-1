from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from django.contrib.sites.models import Site
from datetime import datetime,date,timedelta
from dateutil.tz import gettz
from itertools import compress


class StatsPerWeekMixin(EdcBaseViewMixin):

    @property
    def sites_names(self):
        site_lists = []
        sites = Site.objects.all()
        for site in sites:
            name = site.name.split('-')[1]
            site_lists.append(name)
        return site_lists
    
    
    study_open_datetime = date(
            2021, 4, 15)
    study_close_datetime = date(
            2025, 12, 1)
    
    day = timedelta(days=1)
    list_of_sundays = []
    while study_open_datetime != study_close_datetime:
        study_open_datetime += day
        if study_open_datetime.weekday() == 6:
            list_of_sundays.append(study_open_datetime)
            
    res = list(zip(list_of_sundays, list_of_sundays[1:] + list_of_sundays[:1]))   
    week_list = []
    for value in res:
        res.index(value)+1
        week = [f'Week {res.index(value)+1}',value]
        
        week_list.append(week)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dummy_stats_per_week = [
            ['2021-11-08 to 2021-11-14', '1', '1', '0', '0', '0',   '0'],
            ['2021-12-06 to 2021-12-12', '86', '212', '5', '24', '45', '0'],
            ['2021-12-13 to 2021-12-19', '86', '212', '5', '24', '45', '0'],
            ['Total', '86', '212', '5', '24', '45', '0'],
        ]

        context.update(
            sites=self.sites_names,
            dummy_stats_per_week=dummy_stats_per_week,
            sundays=self.list_of_sundays,
            pairs_dates = self.res,
            pairs_dates_weeks = self.week_list

        )
        return context
