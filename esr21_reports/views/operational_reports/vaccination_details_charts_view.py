from chartjs.views.columns import BaseColumnsHighChartsView

from .vaccination_details_view_mixin import VaccinationDetailsViewMixin


class VaccinationDetailsChartsView(VaccinationDetailsViewMixin,
                                   BaseColumnsHighChartsView):

    title = 'Vaccination details by site'
    yUnit = 'count'

    def get_subtitle(self):
        return '(as per Adverse Event response)'

    def get_yTitle(self):
        return 'Vaccinations (count)'

    def get_labels(self):
        labels = []
        for qs_item in self.overall_vaccination_stats():
            labels.append(f"{qs_item['site__domain']}")
        return labels

    def get_xAxis(self):
        return {'categories': self.get_labels(), 'crosshair': True}

    def get_series(self):
        series = [
            {
                'name': 'Vaccination Details Recorded',
                'data': [qs_item.get('vaccination_details_recorded') for qs_item in self.overall_vaccination_stats()],
                'color': 'green'
            },
            {
                'name': 'AEs Triggered',
                'data': [qs_item.get('adverse_events_triggered') for qs_item in self.overall_vaccination_stats()],
                'color': 'blue'
            },
            {
                'name': 'AEs Not Triggered',
                'data': [qs_item.get('adverse_events_not_triggered') for qs_item in self.overall_vaccination_stats()],
                'color': 'red'
            },
            {
                'name': 'N/A',
                'data': [qs_item.get('adverse_events_na') for qs_item in self.overall_vaccination_stats()],
                'color': 'yellow'
            },
            {
                'name': 'Missing',
                'data': [qs_item.get('adverse_events_missing') for qs_item in self.overall_vaccination_stats()],
                'color': 'grey'
            },
        ]
        return series


vaccination_details_chart_json = VaccinationDetailsChartsView.as_view()
