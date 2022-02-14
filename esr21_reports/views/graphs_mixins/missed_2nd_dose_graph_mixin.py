import pytz
from django.apps import apps as django_apps
from django_pandas.io import read_frame

from edc_base import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin


class Missed2ndDoseGraphMixin(EdcBaseViewMixin):
    appointment_model = 'edc_appointment.appointment'
    consent_model = 'esr21_subject.informedconsent'
    vaccination_details_model = 'esr21_subject.vaccinationdetails'
    sites = [40, 41, 42, 43, 44]

    @property
    def appointment_cls(self):
        return django_apps.get_model(self.appointment_model)

    @property
    def consent_cls(self):
        return django_apps.get_model(self.consent_model)

    @property
    def vaccination_details_cls(self):
        return django_apps.get_model(self.vaccination_details_model)

    @property
    def missed_second_dose(self):
        """Return a list of subject identifiers for participants who missed their
        second dose up to today.
        """
        site_statistics = {
            40: 0,
            41: 0,
            42: 0,
            43: 0,
            44: 0
        }

        missed_second_dose_by_gender = {
            "males": 0,
            "females": 0,
            "others": 0
        }

        for appt in self.appointment_cls.objects.filter(visit_code='1070'):
            latest_start = (appt.timepoint_datetime + appt.visits.get(
                appt.visit_code).rupper).astimezone(pytz.timezone('Africa/Gaborone'))
            try:
                self.vaccination_details_cls.objects.get(
                    subject_visit__subject_identifier=appt.subject_identifier,
                    subject_visit__visit_code='1070',
                    received_dose_before='second_dose'
                )
            except self.vaccination_details_cls.DoesNotExist:
                if latest_start.date() < get_utcnow().date():
                    site_statistics[appt.site_id] += 1
                    consent = self.consent_cls.objects.filter(
                        subject_identifier=appt.subject_identifier).last()
                    if consent:
                        if consent.gender == 'F':
                            missed_second_dose_by_gender['females'] += 1
                        elif consent.gender == 'M':
                            missed_second_dose_by_gender['males'] += 1
                        elif consent.gender == 'OTHER':
                            missed_second_dose_by_gender['others'] += 1
                    else:
                        print(appt.subject_identifier, '**************')
        site_statistics_list = list(map(list, site_statistics.items()))
        return [site_statistics_list, missed_second_dose_by_gender]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            missed_second_dose_by_gender=self.missed_second_dose[1],
            missed_second_dose_by_site=self.missed_second_dose[0]
        )
        return context
