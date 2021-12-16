from django.core.paginator import Paginator
from django.apps import apps as django_apps
from django.views.generic.list import ListView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import EligibilityConfirmation


class ScreeningView(EdcBaseViewMixin, NavbarViewMixin, ListView):
    template_name = 'esr21_reports/operational_reports/screening_report.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'operational_reports'
    model = EligibilityConfirmation

    subject_screening_model = 'esr21_subject.eligibilityconfirmation'

    second_screening_model = 'esr21_subject.screeningeligibility'

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def second_screening_cls(self):
        return django_apps.get_model(self.second_screening_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        screenings = self.subject_screening_cls.objects.all()
        enrollments = self.second_screening_cls.objects.all()
        paginator = Paginator(screenings, 6)
        self.object_list = self.get_queryset()
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        gaborone = screenings.filter(site_id=40).count()
        maun = screenings.filter(site_id=41).count()
        serowe = screenings.filter(site_id=42).count()
        f_town = screenings.filter(site_id=43).count()
        phikwe = screenings.filter(site_id=44).count()

        eligible = screenings.filter(is_eligible=True).count()
        not_eligible = screenings.filter(is_eligible=False).count()
        enrolled = enrollments.filter(is_eligible=True).count()
        not_enrolled = enrollments.filter(is_eligible=False).count()
        total_not_enrolled = not_eligible+not_enrolled

        context.update(
            screenings=screenings,
            page_obj=page_obj,
            object_list=self.object_list,
            gaborone=gaborone,
            maun=maun,
            serowe=serowe,
            phikwe=phikwe,
            f_town=f_town,
            eligible=eligible,
            not_eligible=not_eligible,
            enrolled=enrolled,
            not_enrolled=not_enrolled,
            total_not_enrolled=total_not_enrolled,
        )
        return context
