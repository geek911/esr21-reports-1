from chartjs.views.lines import BaseLineChartView
from calendar import month_name

from django.apps import apps as django_apps
from django.contrib.sites.models import Site


class AdverseEventChartJSONView(BaseLineChartView):
    adverse_event_model = 'esr21_subject.adverseevent'

    @property
    def adverse_events_cls(self):
        return django_apps.get_model(self.adverse_event_model)

    @property
    def months(self):
        adverse_events = self.adverse_events_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.strftime("%B") for vd in adverse_events]
        month_lookup = list(month_name)
        months = list(set(months))
        return sorted(months, key=month_lookup.index)

    @property
    def months_numbers(self):
        adverse_events_details = self.adverse_events_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.month for vd in adverse_events_details]
        months = list(set(months))
        return sorted(months)

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return self.months

    def get_providers(self):
        """Return names of datasets."""
        sites = Site.objects.all().order_by('id')
        return [site.name for site in sites]

    def get_data(self):
        data = []
        sites = Site.objects.all().order_by('id').values_list(
            'id', flat=True).distinct()

        for site_id in sites:
            row_data = []
            experienced_ae_details = self.adverse_events_cls.objects.filter(
                site__id=site_id,
                experienced_ae='Yes')

            for month_num in self.months_numbers:
                temp_experienced_aes = [x for x in experienced_ae_details if x.created.month == month_num]
                row_data.append(len(temp_experienced_aes))
            data.append(row_data)
        return data


adverse_event_chart_json = AdverseEventChartJSONView.as_view()