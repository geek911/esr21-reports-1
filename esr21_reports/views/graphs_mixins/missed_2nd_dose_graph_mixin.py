import pytz
from django.apps import apps as django_apps
from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin


class Missed2ndDoseGraphMixin(EdcBaseViewMixin):
    appointment_model = 'edc_appointment.appointment'
    consent_model = 'esr21_subject.informedconsent'
    sites = [40, 41, 42, 43, 44]

    @property
    def appointment_cls(self):
        return django_apps.get_model(self.appointment_model)

    @property
    def consent_cls(self):
        return django_apps.get_model(self.consent_model)

    @property
    def appt_identifiers(self):
        appt_identifiers = []
        for appt in self.appointment_cls.objects.filter(visit_code='1070'):
            latest_start = (appt.timepoint_datetime + appt.visits.get(
                appt.visit_code).rupper).astimezone(pytz.timezone('Africa/Gaborone'))
            if latest_start < appt.appt_datetime:
                appt_identifiers.append(appt.subject_identifier)
        return appt_identifiers

    @property
    def missed_second_dose_by_site(self):
        missed_second_dose_by_site = []
        for site_id in self.sites:
            appts = self.appointment_cls.objects.filter(
                Q(subject_identifier__in=self.appt_identifiers) & Q(
                    site_id=site_id)).count()
            missed_second_dose_by_site.append(
                appts
            )
        return missed_second_dose_by_site

    @property
    def missed_second_dose_by_gender(self):
        consents = self.consent_cls.objects.filter(
            Q(subject_identifier__in=self.appt_identifiers))

        males = 0
        females = 0
        others = 0
        for consent in consents:
            if consent.gender == 'F':
                females += 1
            elif consent.gender == 'M':
                males += 1
            else:
                others += 1

        missed_second_dose_by_gender = {
            "males": males,
            "females": females,
            "others": others
        }

        return missed_second_dose_by_gender

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            missed_second_dose_by_gender=self.missed_second_dose_by_gender,
            missed_second_dose_by_site=self.missed_second_dose_by_site
        )
        return context
