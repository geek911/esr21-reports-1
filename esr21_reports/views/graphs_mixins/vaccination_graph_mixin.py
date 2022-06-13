from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin


class VaccinationGraphMixin(EdcBaseViewMixin):
    vaccination_details_model = 'esr21_subject.vaccinationdetails'

    @property
    def vaccination_details_cls(self):
        return django_apps.get_model('esr21_subject.vaccinationdetails')

    def site_dose_vaccination(self, site_id=None,  dose=None):
        site_vaccination = self.vaccination_details_cls.objects.filter(
            received_dose_before=dose, site_id=site_id).count()
        return self.get_percentage(site_id, site_vaccination)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        labels = self.sites_names

        context.update(
            vac_details_labels=labels,
            vac_details_first_dose=self.first_dose,
            vac_details_second_dose=self.second_dose,
            all_sites_dose=self.all_sites_dose,
        )
        return context

    def get_percentage(self, site_id, dose):
        site_vaccines = self.vaccination_details_cls.objects.filter(
            site_id=site_id).count()
        percentage = dose / (site_vaccines * 100)
        return percentage
