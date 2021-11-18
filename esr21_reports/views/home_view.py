from django.apps import apps as django_apps
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import EligibilityConfirmation, InformedConsent,VaccinationDetails


class HomeView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'esr21_reports/home.html'
    navbar_selected_item = 'Reports'
    navbar_name = 'esr21_reports'

    subject_screening_model = 'esr21_subject.eligibilityconfirmation'
    subject_consent_model = 'esr21_subject.informedconsent'
    vaccine_model = 'esr21_subject.vaccinationdetails'
    ae_model = 'esr21_subject.adverseeventrecord'
    sae_model = 'esr21_subject.seriousadverseeventrecord'
    siae_model = 'esr21_subject.specialinterestadverseeventrecord'

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consents = self.subject_consent_cls.objects.all().count()
        vaccines = self.vaccine_model_cls.objects.all().count()
        aes = self.ae_cls.objects.all().count()
        saes = self.sae_cls.objects.all().count()
        siaes = self.siae_cls.objects.all().count()
    
        site_screenings = [
            ['Gaborone', 2],
            ['F/Town', 3],
            ['S/Phikwe', 5],
            ['Maun', 2],
            ['Serowe', 4]]

        site_vaccinations = [
            ['Gaborone', 2],
            ['F/Town', 3],
            ['S/Phikwe', 5],
            ['Maun', 2],
            ['Serowe', 4]]
    
        not_erolled = [
            ['Gaborone', 2],
            ['F/Town', 3],
            ['S/Phikwe', 5],
            ['Maun', 2],
            ['Serowe', 4]]
    
        total_screenings = self.subject_screening_cls.objects.all().count()
        total_vaccinations = 0
        total_not_erolled = 0


        context.update(
            total_screenings=total_screenings,
            total_vaccinations=total_vaccinations,
            total_not_erolled=total_not_erolled,
            aes=aes,
            saes=saes,
            siaes=siaes,
            site_screenings=site_screenings,
            site_vaccinations=site_vaccinations,
            not_erolled=not_erolled,
        )

        return context
