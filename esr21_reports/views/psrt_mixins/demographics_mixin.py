from datetime import date
from edc_base.view_mixins import EdcBaseViewMixin
from esr21_subject.models import *
from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_constants.constants import *

class DemographicsMixin(EdcBaseViewMixin):

    def site_ids(self):
        site_ids = Site.objects.order_by('id').values_list('id', flat=True)
        return site_ids


    def enrolled_pids(self):
        enrolled = VaccinationDetails.objects.filter(
            received_dose_before='first_dose').values_list(
            'subject_visit__subject_identifier', flat=True).distinct()
        return enrolled

    def enrolled_statistics(self)->list[int]:
        """
        Total Enrolled, should be vaccinated
        """

        total_enrolled = []

        for site_id in self.site_ids:
            enrolled = VaccinationDetails.objects.filter(
                received_dose_before='first_dose', site_id=site_id).values_list(
                'subject_visit__subject_identifier', flat=True).distinct().count()
            
            total_enrolled.append(enrolled)

        total_enrolled.insert(0, sum(total_enrolled))

        return total_enrolled

    def males_statistics(self) -> list[int]:
        """
        Males enrolled in the study 
        """
        males = []

        for site_id in self.site_ids:

            males_consented = InformedConsent.objects.filter(
                site_id=site_id, gender=MALE, subject_identifier__in=self.enrolled_pids).count()
            males.append(males_consented)

        males.insert(0, sum(males))

        return males

    
    def females_statistics(self) -> list[int]:
        """
        Females enrolled in the study
        """
        females = []

        for site_id in self.site_ids:

            females_consented = InformedConsent.objects.filter(
                site_id=site_id, gender=FEMALE, subject_identifier__in=self.enrolled_pids).count()
            females.append(females_consented)

        females.insert(0, sum(females))

        return females

    
    def _get_age_range(self, site_id, lower_limit_age, upper_limit_age=None)->int:

        total = 0

        if lower_limit_age and upper_limit_age:
            lower_limit_dob = (
                date.today() - relativedelta(years=lower_limit_age)).isoformat()
            upper_limit_dob = (
                date.today() - relativedelta(years=upper_limit_age)).isoformat()
            total = InformedConsent.objects.filter(dob__range=[
                                                upper_limit_dob, lower_limit_dob], site_id=site_id, subject_identifier__in=self.enrolled_pids).count()

        elif lower_limit_age and not upper_limit_age:
            lower_limit_dob = (
                date.today() - relativedelta(years=lower_limit_age)).isoformat()
            total = InformedConsent.objects.filter(
                dob__lte=lower_limit_dob, site_id=site_id, subject_identifier__in=self.enrolled_pids).count()

        return total

    def age_range_statistics(self)-> dict[str, list[int]]:
        age_18_to_30 = []
        age_30_to_40 = []
        age_40_to_50 = []
        age_50_to_60 = []
        age_60_to_70 = []
        age_70_and_above = []

        for site_id in self.site_ids:
  
            totals = self._get_age_range(site_id, 18, 29)
            age_18_to_30.append(totals)

            totals = self._get_age_range(site_id, 30, 39)
            age_30_to_40.append(totals)

            totals = self._get_age_range(site_id, 40, 49)
            age_40_to_50.append(totals)

            totals = self._get_age_range(site_id, 50, 59)
            age_50_to_60.append(totals)

            totals = self._get_age_range(site_id, 60, 69)
            age_60_to_70.append(totals)

            totals = self._get_age_range(site_id, 70)
            age_70_and_above.append(totals)

        age_18_to_30.insert(0, sum(age_18_to_30))
        age_30_to_40.insert(0, sum(age_30_to_40))
        age_40_to_50.insert(0, sum(age_40_to_50))
        age_50_to_60.insert(0, sum(age_50_to_60))
        age_60_to_70.insert(0, sum(age_60_to_70))
        age_70_and_above.insert(0, sum(age_70_and_above))

        return dict(age_18_to_30=age_18_to_30, 
                    age_30_to_40=age_30_to_40, 
                    age_40_to_50=age_40_to_50, 
                    age_50_to_60=age_50_to_60, 
                    age_60_to_70=age_60_to_70,)


    def hiv_statistics(self)-> dict[str, list[int]]:
        hiv_positive = []
        hiv_negative = []
        hiv_unknown = []


        for site_id in self.site_ids:
            enrolled = VaccinationDetails.objects.filter(
                received_dose_before='first_dose', site_id=site_id).values_list(
                'subject_visit__subject_identifier', flat=True).distinct()

            status = POS
            positive = RapidHIVTesting.objects.filter((Q(subject_visit__subject_identifier__in=enrolled) & Q(
                site_id=site_id)) & (Q(hiv_result=status) | Q(rapid_test_result=status))).count()

            status = NEG
            negative = RapidHIVTesting.objects.filter((Q(subject_visit__subject_identifier__in=enrolled) & Q(
                site_id=site_id)) & (Q(hiv_result=status) | Q(rapid_test_result=status))).count()

            status = IND
            unknown = RapidHIVTesting.objects.filter((Q(subject_visit__subject_identifier__in=enrolled) & Q(
                site_id=site_id)) & (Q(hiv_result=status) | Q(rapid_test_result=status))).count()

            hiv_positive.append(positive)
            hiv_negative.append(negative)
            hiv_unknown.append(unknown)


        hiv_positive.insert(0, sum(hiv_positive))
        hiv_negative.insert(0, sum(hiv_negative))
        hiv_unknown.insert(0, sum(hiv_unknown))

        return dict(hiv_positive=hiv_positive, 
                    hiv_positive=hiv_positive, 
                    hiv_unknown=hiv_unknown)

    def smoking_statistics(self) -> dict[str, list[int]]:
        never_smoked = []
        occasional_smoker = []
        current_smoking = []
        previous_smoker = []


        for site_id in self.site_ids:

            never_smoked = MedicalHistory.objects.filter(site_id=site_id, subject_visit__subject_identifier__in=self.enrolled,
                                                        smoking_status='never_smoked').values_list('subject_visit__subject_identifier').distinct().count()
            occasional_smoker = MedicalHistory.objects.filter(site_id=site_id, subject_visit__subject_identifier__in=self.enrolled,
                                                            smoking_status='occasional_smoker').values_list('subject_visit__subject_identifier').distinct().count()
            current_smoking = MedicalHistory.objects.filter(site_id=site_id, subject_visit__subject_identifier__in=self.enrolled,
                                                            smoking_status='current_smoking').values_list('subject_visit__subject_identifier').distinct().count()
            previous_smoker = MedicalHistory.objects.filter(site_id=site_id, subject_visit__subject_identifier__in=self.enrolled,
                                                            smoking_status='previous_smoker').values_list('subject_visit__subject_identifier').distinct().count()

            never_smoked.append(never_smoked)
            occasional_smoker.append(occasional_smoker)
            current_smoking.append(current_smoking)
            previous_smoker.append(previous_smoker)


        never_smoked.insert(0, sum(never_smoked))
        occasional_smoker.insert(0, sum(occasional_smoker))
        current_smoking.insert(0, sum(current_smoking))
        previous_smoker.insert(0, sum(previous_smoker))

        return dict(never_smoked=never_smoked, 
                    occasional_smoker=occasional_smoker, 
                    current_smoking=current_smoking, 
                    previous_smoker=previous_smoker)


    def race_statistics(self) -> dict[str, list[int]]:
        black_african = []
        asian = []
        caucasian = []
        other_race = []

        for site_id in self.site_ids:

            ethnicity_count = DemographicsData.objects.filter(
                ethnicity='Black African', subject_visit__subject_identifier__in=self.enrolled, site_id=site_id).count()
            black_african.append(ethnicity_count)

            ethnicity_count = DemographicsData.objects.filter(
                ethnicity='Asian', subject_visit__subject_identifier__in=self.enrolled, site_id=site_id).count()
            asian.append(ethnicity_count)

            ethnicity_count = DemographicsData.objects.filter(
                ethnicity='Caucasian', subject_visit__subject_identifier__in=self.enrolled, site_id=site_id).count()
            caucasian.append(ethnicity_count)

            ethnicity_count = DemographicsData.objects.filter(
                ethnicity_other__isnull=False, subject_visit__subject_identifier__in=self.enrolled, site_id=site_id).count()
            other_race.append(ethnicity_count)

        black_african.insert(0, sum(black_african))
        asian.insert(0, sum(asian))
        caucasian.insert(0, sum(caucasian))
        other_race.insert(0, sum(other_race))

        return dict(black_african=black_african, 
                    asian=asian, 
                    caucasian=caucasian, 
                    other_race=other_race)




