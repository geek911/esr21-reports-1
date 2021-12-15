from django_pandas.io import read_frame
from django.apps import apps as django_apps
from django.db.models import Count, Q, F
from django.views.generic.base import ContextMixin

from edc_constants.constants import YES, NO, NOT_APPLICABLE


class VaccinationDetailsViewMixin(ContextMixin):

    vaccination_details_model = 'esr21_subject.vaccinationdetails'
    ae_model = 'esr21_subject.adverseevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        overall_vaccination_table = self.overall_vaccination_stats()
        ae_per_response = self.ae_by_reponse()

        context.update(
            overall_vaccination_table=overall_vaccination_table,
            ae_per_response=ae_per_response)
        return context

    def overall_vaccination_stats(self):
        qs = self.vaccination_model_cls.objects.values('site__domain').annotate(
            vaccination_details_recorded=Count('site__domain'),
            adverse_events_triggered=Count('site__domain', filter=Q(adverse_event=YES)),
            adverse_events_not_triggered=Count('site__domain', filter=Q(adverse_event=NO)),
            adverse_events_na=Count('site__domain', filter=Q(adverse_event=NOT_APPLICABLE)),
            adverse_events_missing=Count('site__domain', filter=Q(adverse_event='')))
        return self.replace_site_id_name(qs=qs)

    def ae_by_reponse(self):
        ae_responses_dict = {}
        for response in self.ae_choice_responses:
            ae_response = self.get_ae_per_response(response=response)
            ae_response = self.replace_site_id_name(qs=ae_response)
            ae_responses_dict.update({response: ae_response})
        return ae_responses_dict

    def get_ae_per_response(self, response=None):
        adverse_event = self.ae_model_cls.objects.values_list('subject_visit_id')
        ae_by_response = self.vaccination_model_cls.objects.values('site__domain').annotate(
            adverse_events_expected=Count('site__domain', filter=Q(adverse_event=response)),
            actual_adverse_events=Count('site__domain', filter=(Q(adverse_event=response) & Q(subject_visit_id__in=adverse_event))),
            missing_adverse_events=(F('adverse_events_expected') - F('actual_adverse_events')))
        return ae_by_response

    @property
    def vaccination_model_cls(self):
        return django_apps.get_model(self.vaccination_details_model)

    @property
    def vaccination_model_objs(self):
        return self.vaccination_model_cls.objects.all()

    @property
    def ae_model_cls(self):
        return django_apps.get_model(self.ae_model)

    def qs_to_df(self, queryset=[], fieldnames=[]):
        return read_frame(queryset, fieldnames=fieldnames)

    @property
    def sites_mapping(self):
        site_id_dict = {'esr21': 'Gaborone',
                        'esr21_41': 'Maun',
                        'esr21_42': 'Serowe',
                        'esr21_43': 'Fracistown',
                        'esr21_44': 'Selibe Phikwe'}
        return site_id_dict

    def replace_site_id_name(self, qs=None):
        qs_list = []
        for item in qs:
            qs_list.append({key: self.sites_mapping.get(value, item[key]) for key, value in item.items()})
        return qs_list

    @property
    def ae_choice_responses(self):
        return [YES, NO]
