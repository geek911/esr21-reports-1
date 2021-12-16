from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.views.generic.list import ListView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import SeriousAdverseEvent


class SeriousAdverseEventView(EdcBaseViewMixin, NavbarViewMixin, ListView):
    template_name = 'esr21_reports/safety_reports/sae_detailed_reports.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'Safety Reports'
    model = SeriousAdverseEvent

    sae_model = 'esr21_subject.seriousadverseevent'
    sae_record_model = 'esr21_subject.seriousadverseeventrecord'

    @property
    def sae_cls(self):
        return django_apps.get_model(self.sae_model)

    @property
    def sae_cls_record(self):
        return django_apps.get_model(self.sae_record_model)

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
        saes = self.sae_cls.objects.all()
        saesr = self.sae_cls_record.objects.all()
        all_sites = 'All Sites'

        total_sae = []
        existing_sae_records = []
        missing_saer_records_events_by_site = []

        for site in self.sites:
            total_sae.append([site, self.get_sae_by_site(site)])
            existing_sae_records.append([site, self.get_sae_record_by_site(
                site)])
            missing_saer_records_events_by_site.append(
                [site, self.missing_saer_events_by_site(site)]
            )
        total_sae.append([all_sites, self.get_total_sae()])
        existing_sae_records.append([all_sites, self.get_total_sae_records()])
        missing_saer_records_events_by_site.append(
            [all_sites, self.get_total_missing_sae_records()])

        context.update(
            total_sae=total_sae,
            existing_sae_records=existing_sae_records,
            missing_sae_records=missing_saer_records_events_by_site,
            saesr=saesr,
            saes=saes,
            experienced_sae_events_data=self.get_experienced_sae_events_data(),
            existing_saer_data=self.get_existing_saer_data(),
            missing_saer_data=self.get_missing_saer_data(),
            sites=self.sites,
            test_mis_saer=self.get_no_sae_records(),
        )
        return context

    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endswith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_total_sae(self):
        return self.sae_cls.objects.all().count()

    def get_sae_by_site(self, site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.sae_cls.objects.filter(site_id=site_id).count()

    def get_total_sae_records(self):
        return self.sae_cls_record.objects.count()

    def get_sae_record_by_site(self, site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.sae_cls_record.objects.filter(site_id=site_id).count()

    def missing_saer_events_by_site(self, site_name_postfix=None):
            site_id = self.get_site_id(site_name_postfix)
            if site_id:
                sae = self.sae_cls.objects.filter(site_id=site_id).count()
                saer = self.sae_cls_record.objects.filter(site_id=site_id).count()
                total = sae - saer
                if total > 0:
                    return total
                return 0

    def get_total_missing_sae_records(self):
        total_sae = self.get_total_sae()
        total_sae_records = self.get_total_sae_records()
        total = total_sae - total_sae_records
        if total > 0:
            return total
        return 0

    def get_experienced_sae_events_data(self):
        data = []
        for site in self.sites:
            sae = self.get_sae_by_site(site)
            data.append(sae)
        return data

    def get_existing_saer_data(self):
        data = []
        for site in self.sites:
            saer = self.get_sae_record_by_site(site)
            data.append(saer)
        return data

    def get_missing_saer_data(self):
        data = []
        for site in self.sites:
            missing_saer = self.get_total_missing_sae_records()    
            data.append(missing_saer)
        return data

    def get_no_sae_records(self):
        saes = self.sae_cls_record.objects.all().values_list('serious_adverse_event_id')
        res = self.sae_cls.objects.exclude(id__in=saes)
        return res
