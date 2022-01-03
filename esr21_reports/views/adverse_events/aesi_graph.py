from chartjs.views.lines import BaseLineChartView
from calendar import month_name

from django.apps import apps as django_apps
from django.contrib.sites.models import Site

class AdverseEventOfSpecialInterestChartJSONView(BaseLineChartView):
    aesi_model = 'esr21_subject.specialinterestadverseevent'

    @property
    def aesi_cls(self):
        return django_apps.get_model(self.aesi_model)

    @property
    def months(self):
        aesi = self.aesi_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.strftime("%B") for vd in aesi]
        month_lookup = list(month_name)
        months = list(set(months))
        return sorted(months, key=month_lookup.index)

    @property
    def months_numbers(self):
        aesi_details = self.aesi_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.month for vd in aesi_details]
        months = list(set(months))
        return sorted(months)

    def get_labels(self):
        return self.months

    def get_providers(self):
        sites = Site.objects.order_by('id')
        return [ site.name for site in sites]

    def get_data(self):
        data = []
        sites = Site.objects.all().order_by('id').values_list(
            'id', flat=True).distinct()

        for site_id in sites: 
            row_data = []      
            aesi_details = self.aesi_cls.objects.filter(site__id=site_id)

            for month_num in self.months_numbers:
                aesi_data = [x for x in aesi_details if x.created.month == month_num]
                row_data.append(len(aesi_data))
            data.append(row_data)
        return data


aesi_chart_json = AdverseEventOfSpecialInterestChartJSONView.as_view()