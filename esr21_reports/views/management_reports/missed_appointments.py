import pytz
from django.apps import apps as django_apps
from django.views.generic.base import ContextMixin
from edc_appointment.constants import NEW_APPT
from edc_base.utils import get_utcnow


class MissedAppointmentsMixin(ContextMixin):

    appointment_cls = django_apps.get_model('edc_appointment.appointment')

    def missed_appointments(self, start_date=None, end_date=None):
        appointments = []
        today_dt = get_utcnow()
        for appointment in self.appointment_objs(start_date=start_date, end_date=end_date):
            if today_dt > self.latest_appt_start(appointment=appointment):
                appointments.append(appointment)
        return appointments

    def appointment_objs(self, start_date=None, end_date=None):
        if start_date and end_date:
            return self.appointment_cls.filter(timepoint_datetime__range=(
                start_date, end_date))
        return self.appointment_cls.objects.filter(appt_status=NEW_APPT)

    def latest_appt_start(self, appointment=None):
        latest = None
        if appointment:
            visit_code = appointment.visit_code
            rupper = appointment.visits.get(visit_code).rupper
            timepoint_dt = appointment.timepoint_datetime
            latest = (timepoint_dt + rupper).astimezone(pytz.timezone('Africa/Gaborone'))
        return latest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        missed_appointments = self.missed_appointments()
        context.update(
            missed_appointments=missed_appointments)
        return context
