from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from ..views.adverse_events import (
    AdverseEventRecordViewMixin,SeriousAdverseEventRecordViewMixin)
from .screening_reports_view_mixin import ScreeningReportsViewMixin


class PSRTView(AdverseEventRecordViewMixin,
               SeriousAdverseEventRecordViewMixin,
               ScreeningReportsViewMixin,
               NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'esr21_reports/psrt_report.html'
    navbar_selected_item = 'PSRT Reports'
    navbar_name = 'esr21_reports'

    subject_screening_model = 'esr21_subject.eligibilityconfirmation'
    screening_eligibility_model = 'esr21_subject.screeningeligibility'
    subject_consent_model = 'esr21_subject.informedconsent'
    vaccine_model = 'esr21_subject.vaccinationdetails'
    ae_model = 'esr21_subject.adverseeventrecord'
    sae_model = 'esr21_subject.seriousadverseeventrecord'
    siae_model = 'esr21_subject.specialinterestadverseeventrecord'
    offstudy_model = 'esr21_prn.subjectoffstudy'

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def screening_eligibility_cls(self):
        return django_apps.get_model(self.screening_eligibility_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def vaccine_model_cls(self):
        return django_apps.get_model(self.vaccine_model)

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
    def offstudy_cls(self):
        return django_apps.get_model(self.offstudy_model)

    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endswith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_screened_by_site(self, site_name_postfix):

        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.subject_screening_cls.objects.filter(site_id=site_id).count()

    def get_vaccinated_by_site(self, site_name_postfix):

        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.vaccine_model_cls.objects.filter(received_dose_before='first_dose',
                                                         site_id=site_id).count()

    def get_second_dose_by_site(self, site_name_postfix):

        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.vaccine_model_cls.objects.filter(received_dose_before='second_dose',
                                                         site_id=site_id).count()

    def get_offstudy_by_site(self, site_name_postfix):

        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.offstudy_cls.objects.filter(site_id=site_id).count()

    def get_offstudy_reasons_by_site(self, site_name_postfix):

        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return tuple(set.union(set(self.offstudy_cls.objects.filter(
                site_id=site_id).values_list('reason', flat=True)),
                set(self.offstudy_cls.objects.filter(
                    site_id=site_id).values_list('reason_other', flat=True))))

    def get_offstudy_after_first_dose_by_site(self, site_name_postfix):

        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            offstudy_ids = self.offstudy_cls.objects.filter(
                site_id=site_id).values_list('subject_identifier')

            return self.vaccine_model_cls.objects.filter(
                received_dose_before='first_dose',
                subject_visit__subject_identifier__in=offstudy_ids,
                site_id=site_id).count()

    def get_offstudy_by_dose(self, dose):

        offstudy_ids = self.offstudy_cls.objects.filter().values_list('subject_identifier')

        return self.vaccine_model_cls.objects.filter(
            received_dose_before=dose,
            subject_visit__subject_identifier__in=offstudy_ids).count()

    def get_offstudy_after_second_dose_by_site(self, site_name_postfix):

        site_id = self.get_site_id(site_name_postfix)

        if site_id:
            offstudy_ids = self.offstudy_cls.objects.filter(
                site_id=site_id).values_list('subject_identifier')

            return self.vaccine_model_cls.objects.filter(
                received_dose_before='second_dose',
                subject_visit__subject_identifier__in=offstudy_ids,
                site_id=site_id).count()

    def get_not_enrolled_by_site(self, site_name_postfix):

        site_id = self.get_site_id(site_name_postfix)

        if site_id:

            eligibility_confirmation_failures = self.subject_screening_cls.objects.filter(
                is_eligible=False, site_id=site_id).count()

            screening_eligibility_failures = self.screening_eligibility_cls.objects.filter(
                is_eligible=False, site_id=site_id).count()

            return eligibility_confirmation_failures + screening_eligibility_failures

    def get_total_not_enrolled(self):

        eligibility_confirmation_failures = self.subject_screening_cls.objects.filter(
            is_eligible=False).count()

        screening_eligibility_failures = self.screening_eligibility_cls.objects.filter(
            is_eligible=False).count()

        return eligibility_confirmation_failures + screening_eligibility_failures

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
