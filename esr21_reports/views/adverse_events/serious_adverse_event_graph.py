from chartjs.views.lines import BaseLineChartView
from calendar import month_name

from django.apps import apps as django_apps
from django.contrib.sites.models import Site


class SeriousAdverseEventChartJSONView(BaseLineChartView):
    sae_model = 'esr21_subject.seriousadverseevent'
    sae_record_model = 'esr21_subject.seriousadverseeventrecord'

    @property
    def sae_cls(self):
        return django_apps.get_model(self.sae_model)

    @property
    def sae_record_cls(self):
        return django_apps.get_model(self.sae_record_model)

    @property
    def months(self):
        adverse_events = self.sae_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.strftime("%B") for vd in adverse_events]
        month_lookup = list(month_name)
        months = list(set(months))
        return sorted(months, key=month_lookup.index)

    @property
    def months_numbers(self):
        adverse_events_details = self.sae_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.month for vd in adverse_events_details]
        months = list(set(months))
        return sorted(months)

    def get_labels(self):
        return self.months

    def get_providers(self):
        sites = Site.objects.all().order_by('id')
        return [site.name for site in sites]

    def get_data(self):
        data = []
        sites = Site.objects.all().order_by('id').values_list(
            'id', flat=True).distinct()

        for site_id in sites: 
            row_data = []      
            sae_details = self.sae_cls.objects.filter(site__id=site_id)

            for month_num in self.months_numbers:
                sae_data = [x for x in sae_details if x.created.month == month_num]
                row_data.append(len(sae_data))
            data.append(row_data)
        return data



serious_adverse_event_chart_json = SeriousAdverseEventChartJSONView.as_view()