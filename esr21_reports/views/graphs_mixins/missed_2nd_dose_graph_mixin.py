import pytz
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django_pandas.io import read_frame

from edc_base import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from esr21_metadata_rules.tests.models import InformedConsent


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

    def missed_second_dose(appointment_date=None):
        window_last_date = (appointment_date + relativedelta(days=14)).astimezone(pytz.timezone('Africa/Gaborone'))
        if window_last_date.date() < get_utcnow().date():
            return True
        return False

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

        second_dose = self.vaccination_details_cls.objects.filter(
                    subject_visit__visit_code='1070',
                    received_dose_before='second_dose').values_list('subject_visit__subject_identifier', flat=True)
        second_dose = list(set(second_dose))
        qs = self.appointment_cls.objects.filter(visit_code='1070').exclude(subject_identifier__in=second_dose)
        df = read_frame(qs, fieldnames=['subject_identifier', 'site_id', 'timepoint_datetime'])

        df['missed_second_dose'] = df['timepoint_datetime'].apply(self.missed_second_dose)
        # selecting rows based on condition 
        rslt_df = df[(df['missed_second_dose'] == True)]
        rslt_df.drop_duplicates(subset ="subject_identifier",
                             keep = False, inplace = True)

        subject_identifiers_missed_dose = rslt_df["Name"].tolist()
        
        consent_qs = InformedConsent.objects.filter(subject_identifier__in=subject_identifiers_missed_dose)
        df2 = read_frame(consent_qs, fieldnames=['subject_identifier', 'gender'])
        # dropping ALL duplicate values
        df2.drop_duplicates(subset ="subject_identifier",
                             keep = False, inplace = True)
        df_data = df.merge(df2, on='subject_identifier', how='outer')
        df_data.drop_duplicates(subset ="subject_identifier",
                             keep = False, inplace = True)

        for site_id in sites:
            df_prev = df_data[df_data['site_id'] == site_id]
            site_statistics[appt.site_id] = df_prev[df_prev.columns[0]].count()
    
        male_df = df_data[df_data['gender'] == 'M']
        missed_second_dose_by_gender['males'] = male_df[male_df.columns[0]].count()
        
        female_df = df_data[df_data['gender'] == 'F']
        missed_second_dose_by_gender['females'] = female_df[female_df.columns[0]].count()
    
        others_df = df_data[df_data['gender'] == 'OTHER']
        missed_second_dose_by_gender['others'] = others_df[others_df.columns[0]].count()

        site_statistics_list = list(map(list, site_statistics.items()))
        return [site_statistics_list, missed_second_dose_by_gender]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            missed_second_dose_by_gender=self.missed_second_dose[1],
            missed_second_dose_by_site=self.missed_second_dose[0]
        )
        return context
