from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from .vaccination_details_view_mixin import VaccinationDetailsViewMixin


class VaccinationDetailsStatsView(VaccinationDetailsViewMixin, EdcBaseViewMixin,
                                  NavbarViewMixin, TemplateView):

    template_name = 'esr21_reports/operational_reports/vaccination_details_stats.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'operational_reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
