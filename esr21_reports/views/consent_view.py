from django.core.paginator import Paginator
from django.apps import apps as django_apps
from django.views.generic.list import ListView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import InformedConsent
from edc_constants.constants import YES, NO



class ConsentView(EdcBaseViewMixin, NavbarViewMixin,ListView):
    template_name = 'operational_reports/consent_report.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'Consent Reports'
    model = InformedConsent

    subject_consent_model = 'esr21_subject.informedconsent'

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        consents = self.subject_consent_cls.objects.all()
        paginator = Paginator(consents, 6) # Show 6 contacts per page.
        self.object_list = self.get_queryset()
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        gaborone = consents.filter(site_id=40).count()
        maun = consents.filter(site_id=41).count()
        serowe = consents.filter(site_id=42).count()
        f_town = consents.filter(site_id=43).count()
        phikwe = consents.filter(site_id=44).count()

        eligible = consents.count()

        context.update(
            consents=consents,
            page_obj=page_obj,
            object_list =self.object_list,
            gaborone=gaborone,
            maun=maun,
            serowe=serowe,
            phikwe=phikwe,
            f_town=f_town,
            eligible=eligible,
        )
        return context