
from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from django.contrib.sites.models import Site
from django.db.models import Q


class ScreeningGraphMixin(EdcBaseViewMixin):

    subject_screening_model = 'esr21_subject.eligibilityconfirmation'
    vaccination_model = 'esr21_subject.vaccinationdetails'
    consent_model = 'esr21_subject.informedconsent'

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def vaccination_model_cls(self):
        return django_apps.get_model(self.vaccination_model)

    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.consent_model)

    @property
    def sites_names(self):
        site_lists = []
        sites = Site.objects.all()
        for site in sites:
            name = site.name.split('-')[1]
            site_lists.append(name)
        return site_lists

    @property
    def site_age_dist(self):
        age_dist = []
        for site in self.sites_names:
            age_dist.append([site, self.get_distribution_site(
                site_name_postfix=site)])
        return age_dist

    @property
    def site_screenings(self):
        site_screenings = []
        for site in self.sites_names:
            site_screenings.append([
                site, self.get_screened_by_site(site_name_postfix=site)])
        return site_screenings

    def get_screened_by_site(self, site_name_postfix):
        """Returns a list of a total participants who passed screening and those who
        failed in percentages.
        """
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            eligible_identifiers = self.subject_screening_cls.objects.filter(
                is_eligible=True).values_list('screening_identifier', flat=True)
            eligible_identifiers = list(set(eligible_identifiers))

            consent_screening_ids = self.consent_model_cls.objects.all().values_list(
                'screening_identifier', flat=True)
            consent_screening_ids = list(set(consent_screening_ids))
            no_consent_screenigs = list(set(eligible_identifiers) - set(consent_screening_ids))

            total_screened = self.subject_screening_cls.objects.filter(
                ~Q(screening_identifier__in=no_consent_screenigs))

            all_screening_ids = total_screened.values_list('screening_identifier', flat=True)
            all_screening_ids = list(set(all_screening_ids))

            vaccination = self.vaccination_model_cls.objects.filter(
                Q(received_dose_before='first_dose') | Q(received_dose_before='second_dose')
                ).values_list('subject_visit__subject_identifier', flat=True)
            vaccination = list(set(vaccination))

            passed_screening = self.consent_model_cls.objects.filter(
                subject_identifier__in=vaccination,
                site_id=site_id).values_list('screening_identifier', flat=True)

            passed_screening = list(set(passed_screening))
            failed = total_screened.filter(
                ~Q(screening_identifier__in=passed_screening), site_id=site_id).count()

            total = len(passed_screening)+failed
            passed_screening = round(len(passed_screening)/total * 100, 1)
            failed = round(failed/total * 100, 1)

            return [passed_screening, failed]

    @property
    def overall_screened(self):
        """Returns a list of overall number of participants who passed
        and those who failed screening in percentages.
        """
        eligible_identifiers = self.subject_screening_cls.objects.filter(
            is_eligible=True).values_list('screening_identifier', flat=True)
        eligible_identifiers = list(set(eligible_identifiers))

        consent_screening_ids = self.consent_model_cls.objects.all().values_list('screening_identifier', flat=True)
        consent_screening_ids = list(set(consent_screening_ids))
        no_consent_screenigs = list(set(eligible_identifiers) - set(consent_screening_ids))

        total_screened = self.subject_screening_cls.objects.filter(
            ~Q(screening_identifier__in=no_consent_screenigs))

        all_screening_ids = total_screened.values_list('screening_identifier', flat=True)
        all_screening_ids = list(set(all_screening_ids))

        vaccination = self.vaccination_model_cls.objects.filter(
            Q(received_dose_before='first_dose') | Q(received_dose_before='second_dose')
            ).values_list('subject_visit__subject_identifier', flat=True)
        vaccination = list(set(vaccination))

        passed_screening = self.consent_model_cls.objects.filter(
            Q(subject_identifier__in=vaccination)).values_list(
                'screening_identifier', flat=True)

        passed_screening = list(set(passed_screening))

        failed = total_screened.filter(
            ~Q(screening_identifier__in=passed_screening)).count()

        total = len(passed_screening)+failed

        passed_screening = round(len(passed_screening)/total * 100, 1)
        failed = round(failed/total * 100, 1)

        return [passed_screening, failed]

    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endswith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            site_screenings=self.site_screenings,
            overall_screened=self.overall_screened,
            all_screened_participants=self.all_screened_participants
        )
        return context

    @property
    def all_screened_participants(self):
        return self.subject_screening_cls.objects.count()
