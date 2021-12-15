from django_pandas.io import read_frame
from django.apps import apps as django_apps
from django.db.models import Count, Q
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
        qs_list = []
        qs = self.vaccination_model_cls.objects.values('site__domain').annotate(
            vaccination_details_recorded=Count('site__domain'),
            adverse_events_triggered=Count('site__domain', filter=Q(adverse_event=YES)),
            adverse_events_not_triggered=Count('site__domain', filter=Q(adverse_event=NO)),
            adverse_events_na=Count('site__domain', filter=Q(adverse_event=NOT_APPLICABLE)),
            adverse_events_missing=Count('site__domain', filter=Q(adverse_event='')))
        for item in qs:
            qs_list.append({key: self.sites_mapping.get(value, item[key]) for key, value in item.items()})
        return qs_list

    def ae_by_reponse(self):
        ae_responses_dict = {}
        for response in self.ae_choice_responses:
            ae_by_site = {}
            for site_id, site_name in self.sites_mapping.items():
                ae_response = self.get_ae_per_response(response=response, site=site_id)
                ae_by_site.update({site_name: ae_response})
            ae_responses_dict[response] = ae_by_site
        return ae_responses_dict

    def get_ae_per_response(self, response=None, site=None):
        ae_by_response = self.vaccination_model_objs.filter(
            adverse_event=response, site__domain=site).values_list('subject_visit__id')
        adverse_event = self.ae_model_cls.objects.filter(
            subject_visit__id__in=ae_by_response)
        return [ae_by_response, adverse_event]

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

    @property
    def ae_choice_responses(self):
        return [YES, NO]
