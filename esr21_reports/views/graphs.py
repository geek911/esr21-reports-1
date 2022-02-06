from chartjs.views.lines import BaseLineChartView
from calendar import month_name

from django.apps import apps as django_apps
from django.views.generic import TemplateView
from django.contrib.sites.models import Site


class LineChartJSONView(BaseLineChartView):

    vaccine_model = 'esr21_subject.vaccinationdetails'

    @property
    def vaccine_model_cls(self):
        return django_apps.get_model(self.vaccine_model)

    @property
    def months(self):
        vaccinations_details = self.vaccine_model_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.strftime("%B") for vd in vaccinations_details]
        month_lookup = list(month_name)
        months = list(set(months))
        return sorted(months, key=month_lookup.index)

    @property
    def months_numbers(self):
        vaccinations_details = self.vaccine_model_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.month for vd in vaccinations_details]
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
        sites = Site.objects.all().order_by('id').values_list(
            'id', flat=True).distinct()
        data = []
        for site_id in sites:
            row_data = []
            vaccination_details = self.vaccine_model_cls.objects.filter(
                    site__id=site_id,
                    received_dose_before='first_dose')
            for month_num in self.months_numbers:
                temp_vaccination_details = [vaccine for vaccine in vaccination_details if vaccine.created.month == month_num]
                row_data.append(len(temp_vaccination_details))
            data.append(row_data)
        return data


line_chart = TemplateView.as_view(template_name='esr21_reports/line_chart.html')
line_chart_json = LineChartJSONView.as_view()
