from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.views.generic.list import ListView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import AdverseEvent

from ..model_wrappers import AeModelWrapper


class AdverseEventView(EdcBaseViewMixin, NavbarViewMixin, ListView):
    template_name = 'esr21_reports/safety_reports/ae_reports.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'Safety Reports'
    model = AdverseEvent

    ae_model = 'esr21_subject.adverseevent'
    sae_model = 'esr21_subject.seriousadverseevent'
    siae_model = 'esr21_subject.specialinterestadverseevent'

    ae_record_model = 'esr21_subject.adverseeventrecord'
    sae_record_model = 'esr21_subject.seriousadverseeventrecord'
    siae_record_model = 'esr21_subject.specialinterestadverseeventrecord'

    @property
    def ae_cls(self):
        return django_apps.get_model(self.ae_model)

    @property
    def sae_cls(self):
        return django_apps.get_model(self.sae_model)

    @property
    def siae_cls(self):
        return django_apps.get_model(self.siae_model)

    @property
    def siae_record_cls(self):
        return django_apps.get_model(self.siae_record_model)

    @property
    def ae_record_cls(self):
        return django_apps.get_model(self.ae_record_model)

    @property
    def sae_record_cls(self):
        return django_apps.get_model(self.sae_record_model)

    def get_wrapped_queryset(self, queryset):
        """Returns a list of wrapped model instances.
        """
        object_list = []
        for obj in queryset:
            object_list.append(AeModelWrapper(obj))
        return object_list

    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endswith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_adverse_event_by_site(self,
                                  site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.ae_cls.objects.filter(site_id=site_id).count()

    def get_adverse_event_special_interest_by_site(self,
                                                   site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.siae_cls.objects.filter(site_id=site_id).count()

    def get_serious_adverse_event_by_site(self,
                                          site_name_postfix=None):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.sae_cls.objects.filter(site_id=site_id).count()

    def get_screened_by_site(self, site_name_postfix):

        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.subject_screening_cls.objects.filter(site_id=site_id).count()

    def get_total_aesi(self):
        return self.siae_cls.objects.all().count()

    def get_total_ae(self):
        return self.ae_cls.objects.all().count()

    def get_total_sae(self):
        return self.sae_cls.objects.all().count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        aes = self.ae_record_cls.objects.all()
        saes = self.sae_record_cls.objects.all()
        siaes = self.siae_record_cls.objects.all()

        adverse_events_stats = [
           ['Gaborone', self.get_adverse_event_by_site('Gaborone')],
           ['Maun', self.get_adverse_event_by_site('Maun')],
           ['Serowe', self.get_adverse_event_by_site('Serowe')],
           ['S/Phikwe', self.get_adverse_event_by_site('Phikwe')],
           ['F/Town', self.get_adverse_event_by_site('Francistown')],
           ['All Sites', self.get_total_ae()]
        ]

        serious_adverse_events_stats = [
           ['Gaborone', self.get_serious_adverse_event_by_site('Gaborone')],
           ['Maun', self.get_serious_adverse_event_by_site('Maun')],
           ['Serowe', self.get_serious_adverse_event_by_site('Serowe')],
           ['S/Phikwe', self.get_serious_adverse_event_by_site('Phikwe')],
           ['F/Town', self.get_serious_adverse_event_by_site('Francistown')],
           ['All Sites', self.get_total_sae()]
        ]

        adverse_events_special_interest_stats = [
           ['Gaborone', self.get_adverse_event_special_interest_by_site('Gaborone')],
           ['Maun', self.get_adverse_event_special_interest_by_site('Maun')],
           ['Serowe', self.get_adverse_event_special_interest_by_site('Serowe')],
           ['S/Phikwe', self.get_adverse_event_special_interest_by_site('Phikwe')],
           ['F/Town', self.get_adverse_event_special_interest_by_site('Francistown')],
           ['All Sites', self.get_total_aesi()]
        ]

        ae_medDRA_stats = []
        value_list = aes.values_list('pt_code', flat=True).distinct()

        for ae_number in value_list:
            mild = aes.filter(ae_number=ae_number).filter(ctcae_grade='mild').count()
            moderate = aes.filter(ae_number=ae_number).filter(ctcae_grade='moderate').count()
            severe = aes.filter(ae_number=ae_number).filter(ctcae_grade='severe').count()
            temp = {
                'ae_number': ae_number,
                'mild': mild,
                'moderate': moderate,
                'severe': severe
            }
            ae_medDRA_stats.append(temp)

        context.update(
            object_list=self.object_list,

            aes=aes,
            saes=saes,
            siaes=siaes,

            adverse_events_stats=adverse_events_stats,
            serious_adverse_events_stats=serious_adverse_events_stats,
            adverse_events_special_interest_stats=adverse_events_special_interest_stats,

            ae_medDRA_stats=ae_medDRA_stats,
        )
        return context
