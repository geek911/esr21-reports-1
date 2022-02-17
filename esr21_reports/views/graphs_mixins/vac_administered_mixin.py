from datetime import date

import pytz
from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from edc_base.view_mixins import EdcBaseViewMixin


class VacAdministeredMixin(EdcBaseViewMixin):
    tz = pytz.timezone('Africa/Gaborone')
    created = date.today()
    vaccination_details_model = 'esr21_subject.vaccinationdetails'

    @property
    def vac_details_cls(self):
        return django_apps.get_model('esr21_subject.vaccinationdetails')

    @property
    def vaccinations_first_dose_all_sites(self):
        vaccinations_first_dose_all_sites = self.vac_details_cls.objects.filter(
            received_dose_before='first_dose', created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_first_dose_all_sites = list(set(vaccinations_first_dose_all_sites))
        return len(vaccinations_first_dose_all_sites)

    @property
    def vaccinations_second_dose_all_sites(self):
        vaccinations_second_dose_all_sites = self.vac_details_cls.objects.filter(
            received_dose_before='second_dose', created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_second_dose_all_sites = list(set(vaccinations_second_dose_all_sites))
        return len(vaccinations_second_dose_all_sites)

    # Starts per site
    # Maun
    @property
    def vaccinations_first_maun_sites(self):
        vaccinations_first_maun_sites = self.vac_details_cls.objects.filter(
            received_dose_before='first_dose', site_id=41,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_first_maun_sites = list(set(vaccinations_first_maun_sites))
        return len(vaccinations_first_maun_sites)

    @property
    def vaccinations_second_maun_sites(self):
        vaccinations_second_maun_sites = self.vac_details_cls.objects.filter(
            received_dose_before='second_dose', site_id=41,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_second_maun_sites = list(set(vaccinations_second_maun_sites))
        return len(vaccinations_second_maun_sites)

    # Gaborone
    @property
    def vaccinations_first_gabs_sites(self):
        vaccinations_first_gabs_sites = self.vac_details_cls.objects.filter(
            received_dose_before='first_dose', site_id=40,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_first_gabs_sites = list(set(vaccinations_first_gabs_sites))
        return len(vaccinations_first_gabs_sites)

    @property
    def vaccinations_second_gabs_sites(self):
        vaccinations_second_gabs_sites = self.vac_details_cls.objects.filter(
            received_dose_before='second_dose', site_id=40,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_second_gabs_sites = list(set(vaccinations_second_gabs_sites))
        return len(vaccinations_second_gabs_sites)

    # Serowe
    @property
    def vaccinations_second_serowe_sites(self):
        vaccinations_second_serowe_sites = self.vac_details_cls.objects.filter(
            received_dose_before='second_dose', site_id=42,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_second_serowe_sites = list(set(vaccinations_second_serowe_sites))
        return len(vaccinations_second_serowe_sites)

    @property
    def vaccinations_first_serowe_sites(self):
        vaccinations_first_serowe_sites = self.vac_details_cls.objects.filter(
            received_dose_before='first_dose', site_id=42,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_first_serowe_sites = list(set(vaccinations_first_serowe_sites))
        return len(vaccinations_first_serowe_sites)

    # Ftown
    @property
    def vaccinations_first_ftown_sites(self):
        vaccinations_first_ftown_sites = self.vac_details_cls.objects.filter(
            received_dose_before='first_dose', site_id=43,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_first_ftown_sites = list(set(vaccinations_first_ftown_sites))
        return len(vaccinations_first_ftown_sites)

    @property
    def vaccinations_second_ftown_sites(self):
        vaccinations_second_ftown_sites = self.vac_details_cls.objects.filter(
            received_dose_before='second_dose', site_id=43,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_second_ftown_sites = list(set(vaccinations_second_ftown_sites))
        return len(vaccinations_second_ftown_sites)

    # S/Phikwe
    @property
    def vaccinations_first_phikwe_sites(self):
        vaccinations_first_phikwe_sites = self.vac_details_cls.objects.filter(
            received_dose_before='first_dose', site_id=44,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_first_phikwe_sites = list(set(vaccinations_first_phikwe_sites))
        return len(vaccinations_first_phikwe_sites)

    @property
    def vaccinations_second_phikwe_sites(self):
        vaccinations_second_phikwe_sites = self.vac_details_cls.objects.filter(
            received_dose_before='second_dose', site_id=44,
            created__lte=self.created).values_list(
            'subject_visit__subject_identifier', flat=True)
        vaccinations_second_phikwe_sites = list(set(vaccinations_second_phikwe_sites))
        return len(vaccinations_second_phikwe_sites)

    @property
    def first_dose(self):
        vaccinations_first_gabs_sites_per = self.get_percentage(
            self.vaccinations_first_gabs_sites)

        vaccinations_first_maun_sites_per = self.get_percentage(
            self.vaccinations_first_maun_sites)

        vaccinations_first_serowe_sites_per = self.get_percentage(
            self.vaccinations_first_serowe_sites)

        vaccinations_first_ftown_sites_per = self.get_percentage(
            self.vaccinations_first_ftown_sites)

        vaccinations_first_phikwe_sites_per = self.get_percentage(
            self.vaccinations_first_phikwe_sites)

        first_dose = [
            vaccinations_first_gabs_sites_per,
            vaccinations_first_maun_sites_per,
            vaccinations_first_serowe_sites_per,
            vaccinations_first_ftown_sites_per,
            vaccinations_first_phikwe_sites_per
        ]

        return first_dose

    @property
    def all_sites_dose(self):
        vaccinations_first_dose_all_sites_per = self.get_percentage(
            self.vaccinations_first_dose_all_sites)

        vaccinations_second_dose_all_sites_per = self.get_percentage(
            self.vaccinations_second_dose_all_sites)

        all_sites_dose = [
            vaccinations_first_dose_all_sites_per,
            vaccinations_second_dose_all_sites_per, ]
        return all_sites_dose

    @property
    def sites_names(self):
        site_lists = []
        sites = Site.objects.all()
        for site in sites:
            name = site.name.split('-')[1]
            site_lists.append(name)
        return site_lists

    @property
    def second_dose(self):
        vaccinations_second_gabs_sites_per = self.get_percentage(
            self.vaccinations_second_gabs_sites)

        vaccinations_second_maun_sites_per = self.get_percentage(
            self.vaccinations_second_maun_sites)

        vaccinations_second_serowe_sites_per = self.get_percentage(
            self.vaccinations_second_serowe_sites)

        vaccinations_second_ftown_sites_per = self.get_percentage(
            self.vaccinations_second_ftown_sites)

        vaccinations_second_phikwe_sites_per = self.get_percentage(
            self.vaccinations_second_phikwe_sites)

        second_dose = [
            vaccinations_second_gabs_sites_per,
            vaccinations_second_maun_sites_per,
            vaccinations_second_serowe_sites_per,
            vaccinations_second_ftown_sites_per,
            vaccinations_second_phikwe_sites_per
        ]

        return second_dose

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

    def get_percentage(self, dose):
        percentage = dose / (
                self.vaccinations_first_dose_all_sites + self.vaccinations_second_dose_all_sites) * 100

        return percentage
