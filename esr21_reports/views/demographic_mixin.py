from esr21_subject.models import *

from edc_constants.constants import *
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta



class DemographicStatisticsMixin:
    site_ids = dict(gaborone=40, maun=41, serowe=42, ftown=43, phikwe=44)


    def __init__(self) -> None:
        self.site_ids = dict(gaborone=40, maun=41,
                             serowe=42, ftown=43, phikwe=44)


    def get_first_screening_statistics(self):
        """
        First Screening information
        """


        first_screening_statistics = {
            "total_screened": [],
            "enrolled": [],
            "screening_failure": []
        }

        for site_id in self.site_ids.values():

            total_screened = EligibilityConfirmation.objects.filter(
                site_id=site_id).count()  # screened per site
            enrolled = EligibilityConfirmation.objects.filter(
                site_id=site_id, is_eligible=True).count()  # all eligible
            screening_failure = EligibilityConfirmation.objects.filter(
                site_id=site_id).count()  # screening failure

            first_screening_statistics["total_screened"].append(total_screened)
            first_screening_statistics["enrolled"].append(enrolled)
            first_screening_statistics["screening_failure"].append(screening_failure)
        
        return first_screening_statistics

    def get_second_screening_statistics(self):
        """
        Second Screening information
        """


        second_screening_statistics = {
            "total_screened": [],
            "enrolled": [],
            "screening_failure": []
        }

        for site_id in self.site_ids.values():

            total_screened = ScreeningEligibility.objects.filter(
                site_id=site_id).count()  # screened per site
            enrolled = ScreeningEligibility.objects.filter(
                site_id=site_id, is_eligible=True).count()  # all eligible
            screening_failure = ScreeningEligibility.objects.filter(
                site_id=site_id).count()  # screening failure

            second_screening_statistics["total_screened"].append(total_screened)
            second_screening_statistics["enrolled"].append(enrolled)
            second_screening_statistics["screening_failure"].append(screening_failure)


        return second_screening_statistics


    def get_first_screen_ineligible_statistics(self):
        """
        First Screening failures
        """


        screening_failure_statistics = dict()

        raw_reasons = EligibilityConfirmation.objects.filter(
            is_eligible=False).values_list('ineligibility', flat=True).distinct()

        temp = []

        for reason in raw_reasons:
            temp.extend(eval(reason))

        reasons = set(temp)

        for reason in reasons:
            screening_failure_statistics[reason] = []
            for site_id in self.site_ids.values():
                count = EligibilityConfirmation.objects.filter(
                    ineligibility__icontains=reason, site_id=site_id).count()
                screening_failure_statistics[reason].append(count)

        return screening_failure_statistics

    def get_second_screen_ineligible(self):
        """
        Second Screening failures
        """


        screening_failure_statistics = dict()

        raw_reasons = ScreeningEligibility.objects.filter(
            is_eligible=False).values_list('ineligibility', flat=True).distinct()

        temp = []

        for reason in raw_reasons:
            temp.extend(eval(reason))

        reasons = set(temp)

        for reason in reasons:
            screening_failure_statistics[reason] = []
            for site_id in self.site_ids.values():
                count = ScreeningEligibility.objects.filter(
                    ineligibility__icontains=reason, site_id=site_id).count()
                screening_failure_statistics[reason].append(count)

        return screening_failure_statistics

    def get_demographic_statistics(self):
        demographics_statistics = {
            'Total Consented': [],  # total consented
            'Total Females': [],
            'Total Males': [],
            'Total Enrolled': [],  # eligible after second screening
            '18 <= x < 30': [],
            '30 <= x < 40': [],
            '40 <= x < 50': [],
            '50 <= x < 60': [],
            '60 <= x < 70': [],
            ' >= 70': [],

        }


        #ethnicities
        raw_ethnicities = DemographicsData.objects.values_list(
            'ethnicity', flat=True).distinct()

        for ethnicity in raw_ethnicities:
            demographics_statistics[ethnicity] = []

            for site_id in self.site_ids.values():
                ethnicity_count = DemographicsData.objects.filter(
                    ethnicity=ethnicity, site_id=site_id).count()
                demographics_statistics[ethnicity].append(ethnicity_count)

        # education
        raw_highest_education = DemographicsData.objects.values_list(
            'highest_education', flat=True).distinct()

        for highest_education in raw_highest_education:
            demographics_statistics[highest_education] = []

            for site_id in self.site_ids.values():
                highest_education_count = DemographicsData.objects.filter(
                    highest_education=highest_education, site_id=site_id).count()
                demographics_statistics[highest_education].append(
                    highest_education_count)


        # employement_status
        raw_employment_status = DemographicsData.objects.values_list(
            'employment_status', flat=True).distinct()

        for employment_status in raw_employment_status:
            demographics_statistics[employment_status] = []

            for site_id in site_ids.values():
                employment_status_count = DemographicsData.objects.filter(
                    employment_status=employment_status, site_id=site_id).count()
                demographics_statistics[employment_status].append(
                    employment_status_count)


        # various data
        for site_id in site_ids.values():

            total_enrolled = InformedConsent.objects.filter(
                site_id=site_id).count()  # enrolled
            total_consented = InformedConsent.objects.filter(
                site_id=site_id).count()  # consented
            total_females = InformedConsent.objects.filter(
                site_id=site_id, gender=FEMALE).count()  # gender
            total_males = InformedConsent.objects.filter(
                site_id=site_id, gender=MALE).count()  # females

            demographics_statistics['Total Enrolled'].append(total_enrolled)
            demographics_statistics['Total Consented'].append(total_consented)
            demographics_statistics['Total Females'].append(total_females)
            demographics_statistics['Total Males'].append(total_males)

        subject_identifiers = ScreeningEligibility.objects.filter(
            is_eligible=True).only('subject_identifier').values_list('subject_identifier')


        def get_age_range_stats(lower_age, upper_age, site):
            return InformedConsent.objects.filter(
                dob__range=[lower_age, upper_age], subject_identifier__in=subject_identifiers, site_id=site).only('dob').count()


        for site_id in self.site_ids.values():

            today = date.today()

            age_18 = (today - relativedelta(years=18)).isoformat()
            age_30 = (today - relativedelta(years=29)
                    ).isoformat()  # 30 should be exclusive
            stat = get_age_range_stats(age_18, age_30, site_id)

            demographics_statistics['18 <= x < 30'].append(stat)

            age_30 = (today - relativedelta(years=30)).isoformat()
            age_40 = (today - relativedelta(years=39)).isoformat()
            stat = get_age_range_stats(age_30, age_40, site_id)
            demographics_statistics['30 <= x < 40'].append(stat)

            age_40 = (today - relativedelta(years=40)).isoformat()
            age_50 = (today - relativedelta(years=49)).isoformat()
            stat = get_age_range_stats(age_40, age_50, site_id)
            demographics_statistics['40 <= x < 50'].append(stat)

            age_50 = (today - relativedelta(years=50)).isoformat()
            age_60 = (today - relativedelta(years=59)).isoformat()
            stat = get_age_range_stats(age_50, age_60, site_id)
            demographics_statistics['50 <= x < 60'].append(stat)

            age_60 = (today - relativedelta(years=60)).isoformat()
            age_70 = (today - relativedelta(years=69)).isoformat()
            stat = get_age_range_stats(age_60, age_70, site_id)
            demographics_statistics['60 <= x < 70'].append(stat)

            age_70 = (today - relativedelta(years=70)).isoformat()
            demographics_statistics[' >= 70'].append(stat)

            return demographics_statistics
