from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.views.generic.list import ListView

from edc_navbar import NavbarViewMixin
from edc_base.view_mixins import EdcBaseViewMixin
from esr21_subject.models import SpecialInterestAdverseEvent


class SeriousAdverseEvent(EdcBaseViewMixin, NavbarViewMixin, ListView):
    template_name = 'esr21_reports/safety_reports/siae_detailed_reports.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'Safety Reports'
    model = SpecialInterestAdverseEvent

    siae_model = 'esr21_subject.specialinterestadverseevent'
    siae_record_model = 'esr21_subject.specialinterestadverseeventrecord'

    @property
    def saie_cls(self):
        return django_apps.get_model(self.siae_model)

    @property
    def saie_record_cls(self):
        return django_apps.get_model(self.siae_record_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_siae = [
            ['Gaborone', self.get_serious_adverse_events_by_site('Gaborone')],
            ['Maun', self.get_serious_adverse_events_by_site('Maun')],
            ['Serowe', self.get_serious_adverse_events_by_site('Serowe')],
            ['S/Phikwe', self.get_serious_adverse_events_by_site('Phikwe')],
            ['F/Town', self.get_serious_adverse_events_by_site('Francistown')],
            ['All Sites', self.get_total_siae()]
        ]

        missing_siae_records = [
            ['Gaborone', self.get_missing_adverse_event_record('Gaborone')],
            ['Maun', self.get_missing_adverse_event_record('Maun')],
            ['Serowe', self.get_missing_adverse_event_record('Serowe')],
            ['S/Phikwe', self.get_missing_adverse_event_record('Phikwe')],
            ['F/Town', self.get_missing_adverse_event_record('Francistown')],
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

        )
        return context

    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endwith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_total_siae(self):
        return self.siae_cls.objects.all().count()

    def get_siae_by_site(self, site_name_postfix=None):
        site_id = self.get_site_id(self, site_name_postfix)
        if site_id:
            return self.siae_cls.filter(site_id=site_id).count()

    def get_total_siae_records(self):
        return self.siae_cls_record.objects.count()

    def get_siae_record_by_site(self, site_name_postfix=None):
        site_id = self.get_site_id(self, site_name_postfix)
        if site_id:
            return self.siae_cls_record.filter(site_id=site_id).count()

    def get_total_missing_siae_records(self):
        total_siae = self.get_total_siae()
        total_siae_records = self.get_total_siae_records()
        total = total_siae - total_siae_records
        if total > 0:
            return total
        return 0

    def get_missing_sa_event_record(self,site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            total_site_aes = self.get_siae_record_by_site(site_name_postfix)
            dist_sae_records = self.sae_record_cls.objects.filter(site_id=site_id).values_list('adverse_event', flat=True).distinct().count()
            total = total_site_aes - dist_sae_records
            if total > 0:
                return total
            return 0