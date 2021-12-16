from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.views.generic.list import ListView

from edc_navbar import NavbarViewMixin
from edc_base.view_mixins import EdcBaseViewMixin
from esr21_subject.models import SpecialInterestAdverseEvent


class SpecialInterestAdverseEventView(EdcBaseViewMixin, NavbarViewMixin, ListView):
    template_name = 'esr21_reports/safety_reports/siae_detailed_reports.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'Safety Reports'
    model = SpecialInterestAdverseEvent

    siae_model = 'esr21_subject.specialinterestadverseevent'
    siae_record_model = 'esr21_subject.specialinterestadverseeventrecord'

    @property
    def siae_cls(self):
        return django_apps.get_model(self.siae_model)

    @property
    def saie_record_cls(self):
        return django_apps.get_model(self.siae_record_model)

    @property
    def sites(self):
        sites = Site.objects.all().order_by('id')
        temp_sites = []
        for site in sites:
            site_name = site.name.split('-')[1].strip("&#x27;")
            temp_sites.append(site_name)
        return temp_sites    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_siae = [
            ['Gaborone', self.get_siae_by_site('Gaborone')],
            ['Maun', self.get_siae_by_site('Maun')],
            ['Serowe', self.get_siae_by_site('Serowe')],
            ['S/Phikwe', self.get_siae_by_site('Phikwe')],
            ['F/Town', self.get_siae_by_site('Francistown')],
            ['All Sites', self.get_total_siae()]
        ]

        missing_siae_records = [
            ['Gaborone', self.missing_saer_events_by_site('Gaborone')],
            ['Maun', self.missing_saer_events_by_site('Maun')],
            ['Serowe', self.missing_saer_events_by_site('Serowe')],
            ['S/Phikwe', self.missing_saer_events_by_site('Phikwe')],
            ['F/Town', self.missing_saer_events_by_site('Francistown')],
            ['All Sites', self.get_total_missing_siae_records()]
        ]

        existing_siae_records = [
            ['Gaborone', self.get_siae_record_by_site('Gaborone')],
            ['Maun', self.get_siae_record_by_site('Maun')],
            ['Serowe', self.get_siae_record_by_site('Serowe')],
            ['S/Phikwe', self.get_siae_record_by_site('Phikwe')],
            ['F/Town', self.get_siae_record_by_site('Francistown')],
            ['All Sites', self.get_total_siae_records()]

        ]

        # context
        context.update(
            sites=self.sites,
            total_siae = total_siae,
            missing_siae_records = missing_siae_records,
            existing_siae_records = existing_siae_records,
            experienced_siae_events_data = self.get_experienced_sae_events_data(),
            existing_siaer_data = self.get_existing_siaer_data()

        )
        return context

    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endswith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_total_siae(self):
        return self.siae_cls.objects.all().count()

    def get_siae_by_site(self, site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.siae_cls.objects.filter(site_id=site_id).count()

    def get_total_siae_records(self):
        return self.saie_record_cls.objects.count()

    def get_siae_record_by_site(self, site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.saie_record_cls.objects.filter(site_id=site_id).count()

    def get_total_missing_siae_records(self):
        total_siae = self.get_total_siae()
        total_siae_records = self.get_total_siae_records()
        total = total_siae - total_siae_records
        if total > 0:
            return total
        return 0

    def missing_saer_events_by_site(self, site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            sae = self.siae_cls.objects.filter(site_id=site_id).count()
            saer = self.saie_record_cls.objects.filter(site_id=site_id).count()
            total = sae - saer
            if total > 0:
                return total
            return 0

    def get_experienced_sae_events_data(self):
        data = []
        for site in self.sites:
            sae = self.get_siae_by_site(site)
            data.append(sae)
        return data 

    def get_existing_siaer_data(self):
        data = []
        for site in self.sites:
            saer = self.get_siae_record_by_site(site)
            data.append(saer)
        return data           