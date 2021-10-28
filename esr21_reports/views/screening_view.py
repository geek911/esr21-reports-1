from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import EligibilityConfirmation



class ScreeningView(EdcBaseViewMixin, NavbarViewMixin,ListView):
    template_name = 'operational_reports/screening_report.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'Screening Reports'
    model = EligibilityConfirmation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        screenings = EligibilityConfirmation.objects.all()
        paginator = Paginator(screenings, 6) # Show 6 contacts per page.
        self.object_list = self.get_queryset()
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        gaborone = len([ screening for screening in screenings if screening.site_id == 40 ])
        maun = len([ screening for screening in screenings if screening.site_id == 41 ])
        serowe = len([ screening for screening in screenings if screening.site_id == 42 ])
        phikwe = len([ screening for screening in screenings if screening.site_id == 44 ])
        f_town = len([ screening for screening in screenings if screening.site_id == 43 ])

        eligible = len([ screening for screening in screenings if screening.is_eligible])
        not_eligible = len([ screening for screening in screenings if not screening.is_eligible])

        context.update(
            screenings=screenings,
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