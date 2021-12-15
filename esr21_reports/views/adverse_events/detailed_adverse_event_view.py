from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.views.generic.list import ListView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import AdverseEvent


class DetailedAdverseEventView(EdcBaseViewMixin, NavbarViewMixin, ListView):
    template_name = 'esr21_reports/safety_reports/ae_detailed_reports.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'Safety Reports'
    model = AdverseEvent

    ae_model = 'esr21_subject.adverseevent'
    ae_record_model = 'esr21_subject.adverseeventrecord'

    @property
    def ae_cls(self):
        return django_apps.get_model(self.ae_model)

    @property
    def ae_record_cls(self):
        return django_apps.get_model(self.ae_record_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        experienced_ae = [
           ['Gaborone', self.get_adverse_event_experienced('Gaborone')],
           ['Maun', self.get_adverse_event_experienced('Maun')],
           ['Serowe', self.get_adverse_event_experienced('Serowe')],
           ['S/Phikwe', self.get_adverse_event_experienced('Phikwe')],
           ['F/Town', self.get_adverse_event_experienced('Francistown')],
           ['All Sites', self.get_total_ae_experienced()]
        ]

        not_experienced_ae = [
           ['Gaborone', self.get_adverse_event_not_experienced('Gaborone')],
           ['Maun', self.get_adverse_event_not_experienced('Maun')],
           ['Serowe', self.get_adverse_event_not_experienced('Serowe')],
           ['S/Phikwe', self.get_adverse_event_not_experienced('Phikwe')],
           ['F/Town', self.get_adverse_event_not_experienced('Francistown')],
           ['All Sites', self.get_total_ae_not_experienced()]
        ]

        total_ae = [
           ['Gaborone', self.get_adverse_event_by_site('Gaborone')],
           ['Maun', self.get_adverse_event_by_site('Maun')],
           ['Serowe', self.get_adverse_event_by_site('Serowe')],
           ['S/Phikwe', self.get_adverse_event_by_site('Phikwe')],
           ['F/Town', self.get_adverse_event_by_site('Francistown')],
           ['All Sites', self.get_total_ae()]
        ]

        expected_ae_records = [
           ['Gaborone', self.get_expected_adverse_event_record('Gaborone')],
           ['Maun', self.get_expected_adverse_event_record('Maun')],
           ['Serowe', self.get_expected_adverse_event_record('Serowe')],
           ['S/Phikwe', self.get_expected_adverse_event_record('Phikwe')],
           ['F/Town', self.get_expected_adverse_event_record('Francistown')],
           ['All Sites', self.get_total_expected_ae_records()]
        ]

        unexpected_ae_records = [
           ['Gaborone', self.get_unexpected_adverse_event_record('Gaborone')],
           ['Maun', self.get_unexpected_adverse_event_record('Maun')],
           ['Serowe', self.get_unexpected_adverse_event_record('Serowe')],
           ['S/Phikwe', self.get_unexpected_adverse_event_record('Phikwe')],
           ['F/Town', self.get_unexpected_adverse_event_record('Francistown')],
           ['All Sites', self.get_total_unexpected_ae_records()]
        ]

        missing_ae_records = [
           ['Gaborone', self.get_missing_adverse_event_record('Gaborone')],
           ['Maun', self.get_missing_adverse_event_record('Maun')],
           ['Serowe', self.get_missing_adverse_event_record('Serowe')],
           ['S/Phikwe', self.get_missing_adverse_event_record('Phikwe')],
           ['F/Town', self.get_missing_adverse_event_record('Francistown')],
           ['All Sites', self.get_total_missing_ae_records()]
        ]

        context.update(
            experienced_ae=experienced_ae,
            not_experienced_ae=not_experienced_ae,
            total_ae=total_ae,
            expected_ae_records=expected_ae_records,
            unexpected_ae_records=unexpected_ae_records,
            missing_ae_records=missing_ae_records,
            experienced_ae_events_data=self.get_experienced_ae_events_data(),
            not_experienced_ae_events_data=self.get_not_experienced_ae_events_data(),
            sites=self.sites,
            all_ae_experienced=self.get_all_adverse_event_experienced(),
            all_ae_not_experienced=self.get_all_adverse_event_not_experienced(),
            all_ae_record=self.get_all_adverse_event_record_experienced(),
            all_missing_ae_record=self.get_all_adverse_event_record_missed()
        )
        return context

    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endswith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_adverse_event_by_site(self, site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.ae_cls.objects.filter(site_id=site_id).count()

    def get_total_ae(self):
        return self.ae_cls.objects.all().count()

    def get_total_ae_experienced(self):
        return self.ae_cls.objects.filter(experienced_ae='Yes').count()

    def get_total_ae_not_experienced(self):
        return self.ae_cls.objects.filter(experienced_ae='No').count()

    def get_total_expected_ae_records(self):
        return self.ae_record_cls.objects.filter(
            adverse_event__experienced_ae='Yes').count()

    def get_total_unexpected_ae_records(self):
        return self.ae_record_cls.objects.filter(
            adverse_event__experienced_ae='No').count()

    def get_total_distict_ae_from_ae_records(self):
        return self.ae_record_cls.objects.all().values_list(
            'adverse_event', flat=True).distinct().count()

    def get_total_missing_ae_records(self):
        total_ae = self.get_total_ae_experienced()
        total_ae_records = self.get_total_distict_ae_from_ae_records()
        total = total_ae - total_ae_records
        if total > 0:
            return total
        return 0

    def get_all_adverse_event_experienced(self,):
        return self.ae_cls.objects.filter(experienced_ae='Yes')

    def get_all_adverse_event_not_experienced(self,):
        return self.ae_cls.objects.filter(experienced_ae='No')

    def get_all_adverse_event_record_experienced(self,):
        return self.ae_record_cls.objects.filter(adverse_event__experienced_ae='Yes')

    def get_all_adverse_event_record_missed(self,):
        return self.ae_record_cls.objects.filter(adverse_event__experienced_ae='No')

    def get_adverse_event_experienced(self,
                                      site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.ae_cls.objects.filter(site_id=site_id).filter(
                experienced_ae='Yes').count()

    def get_adverse_event_not_experienced(self,
                                          site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.ae_cls.objects.filter(site_id=site_id).filter(
                experienced_ae='No').count()

    def get_expected_adverse_event_record(self,
                                          site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.ae_record_cls.objects.filter(site_id=site_id).filter(
                adverse_event__experienced_ae='Yes').count()

    def get_unexpected_adverse_event_record(self,
                                            site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.ae_record_cls.objects.filter(site_id=site_id).filter(
                adverse_event__experienced_ae='No').count()

    def get_missing_adverse_event_record(self,
                                         site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            total_site_aes = self.get_adverse_event_experienced(
                site_name_postfix)
            dist_ae_records = self.ae_record_cls.objects.filter(
                site_id=site_id).values_list('adverse_event',
                                             flat=True).distinct().count()
            total = total_site_aes - dist_ae_records
            if total > 0:
                return total
            return 0

    def get_experienced_ae_events_data(self):
        data = []
        for site in self.sites:
            ae = self.get_expected_adverse_event_record(site)
            data.append(ae)
        return data

    def get_not_experienced_ae_events_data(self):
        data = []
        for site in self.sites:
            ae = self.get_unexpected_adverse_event_record(site)
            data.append(ae)
        return data

    @property
    def sites(self):
        sites = Site.objects.all().order_by('id')
        temp_sites = []
        for site in sites:
            site_name = site.name.split('-')[1].strip("&#x27;")
            temp_sites.append(site_name)
        return temp_sites
