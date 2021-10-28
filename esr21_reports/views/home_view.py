from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import EligibilityConfirmation,InformedConsent,VaccinationDetails




class HomeView(NavbarViewMixin,EdcBaseViewMixin,TemplateView):
    template_name = 'home.html'
    navbar_selected_item = 'Reports'
    navbar_name = 'esr21_reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screenings = EligibilityConfirmation.objects.all().count()
        consents = InformedConsent.objects.all().count()
        vaccines = VaccinationDetails.objects.all().count()

        context.update(
            screenings=screenings,
            consents=consents,
            vaccines=vaccines
        )

        return context
