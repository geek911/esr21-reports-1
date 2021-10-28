from django.core.paginator import Paginator
from django.views.generic import TemplateView
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        consents = InformedConsent.objects.all()
        paginator = Paginator(consents, 6) # Show 6 contacts per page.
        self.object_list = self.get_queryset()
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        gaborone = len([consent for consent in consents if consent.site_id == 40 ])
        maun = len([consent for consent in consents if consent.site_id == 41 ])
        serowe = len([consent for consent in consents if consent.site_id == 42 ])
        phikwe = len([consent for consent in consents if consent.site_id == 44 ])
        f_town = len([consent for consent in consents if consent.site_id == 43 ])

        eligible = len([consent for consent in consents if consent.consent_to_participate == YES ])
        not_eligible = len([consent for consent in consents if consent.consent_to_participate == NO ])

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
            not_eligible=not_eligible
        )
        return context