from django.core.paginator import Paginator
from django.apps import apps as django_apps
from django.views.generic.list import ListView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import VaccinationDetails
from edc_constants.constants import NO, YES



class VaccinationView(EdcBaseViewMixin, NavbarViewMixin,ListView):
    template_name = 'operational_reports/vaccination_report.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'Vaccination Reports'
    model = VaccinationDetails

    vaccine_model = 'esr21_subject.vaccinationdetails'

    
    @property
    def vaccine_model_cls(self):
        return django_apps.get_model(self.vaccine_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        vaccines = self.vaccine_model_cls.objects.all()
        paginator = Paginator(vaccines, 6) # Show 6 contacts per page.
        self.object_list = self.get_queryset()
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        gaborone = len([ vaccine for vaccine in vaccines if vaccine.site_id == 40 ])
        maun = len([ vaccine for vaccine in vaccines if vaccine.site_id == 41 ])
        serowe = len([ vaccine for vaccine in vaccines if vaccine.site_id == 42 ])
        phikwe = len([ vaccine for vaccine in vaccines if vaccine.site_id == 44 ])
        f_town = len([ vaccine for vaccine in vaccines if vaccine.site_id == 43 ])

        first_dose = len([ vaccine for vaccine in vaccines if vaccine.received_dose==YES and vaccine.received_dose_before=='first_dose'])
        second_dose = len([ vaccine for vaccine in vaccines if vaccine.received_dose==YES and vaccine.received_dose_before=='second_dose'])
        not_vaccinated = len([ vaccine for vaccine in vaccines if vaccine.received_dose==NO])
        context.update(
            vaccines=vaccines,
            page_obj=page_obj,
            object_list =self.object_list,
            gaborone=gaborone,
            maun=maun,
            serowe=serowe,
            phikwe=phikwe,
            f_town=f_town,
            first_dose=first_dose,
            second_dose=second_dose,
            not_vaccinated=not_vaccinated,
        )
        return context