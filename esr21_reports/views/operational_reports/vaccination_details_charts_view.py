from chartjs.views.columns import BaseColumnsHighChartsView

from .vaccination_details_stats_view_mixin import VaccinationDetailsViewMixin
from edc_constants.constants import YES


class VaccinationDetailsChartsView(VaccinationDetailsViewMixin,
                                   BaseColumnsHighChartsView):

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

    def get_title(self):
        return [{'text': 'Vaccination details by site'},
                {'text': 'Adverse events triggered from vaccination details'},
                {'text': 'Adverse events not triggered from vaccination details'},]

    def get_series(self):
        series = []
        series.append([
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
        ])

        count = 1
        for choice in self.ae_choice_responses:
            count += 1
            series.append([
                {
                    'name': 'Expected AEs' if choice == YES else 'AEs not triggered',
                    'data': [qs_item.get('adverse_events_expected') for qs_item in self.ae_by_reponse().get(choice, [])],
                    'color': 'green'
                },
                {
                    'name': 'Actual AEs' if choice == YES else 'Unexpected AEs',
                    'data': [qs_item.get('actual_adverse_events') for qs_item in self.ae_by_reponse().get(choice, [])],
                    'color': 'blue'
                },
                {
                    'name': 'Missing AEs' if choice == YES else 'AEs accurately No',
                    'data': [qs_item.get('missing_adverse_events') for qs_item in self.ae_by_reponse().get(choice, [])],
                    'color': 'red'
                },
            ])
        return series


vaccination_details_chart_json = VaccinationDetailsChartsView.as_view()
