from django.apps import apps as django_apps

from django.db.models import Q, Count
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import NEG, POS, YES, NO


class SeriousAdverseEventRecordViewMixin(EdcBaseViewMixin):

    sae_record_model = 'esr21_subject.seriousadverseeventrecord'
    ae_record_model = 'esr21_subject.adverseeventrecord'
    rapid_hiv_testing_model = 'esr21_subject.rapidhivtesting'
    vaccination_detail_model = 'esr21_subject.vaccinationdetails'
    consent_model = 'esr21_subject.informedconsent'
    demographics_data_model = 'esr21_subject.demographicsdata'

    @property
    def sae_record_cls(self):
        return django_apps.get_model(self.sae_record_model)

    @property
    def demographics_data_cls(self):
        return django_apps.get_model(self.demographics_data_model)

    @property
    def ae_record_cls(self):
        return django_apps.get_model(self.ae_record_model)

    @property
    def consent_cls(self):
        return django_apps.get_model(self.consent_model)

    @property
    def vaccination_detail_cls(self):
        return django_apps.get_model(self.vaccination_detail_model)

    @property
    def rapid_hiv_testing_cls(self):
        return django_apps.get_model(self.rapid_hiv_testing_model)

    @property
    def sae_overral_adverse_events(self):

        alll_sae_ids = self.sae_record_cls.objects.all().values_list(
            'serious_adverse_event__subject_visit__subject_identifier', flat=True)

        q = Q(adverse_event__subject_visit__subject_identifier__in=alll_sae_ids)

        overral_soc = self.ae_record_cls.objects.filter(q).values('soc_name').annotate(
            total=Count('soc_name', filter=Q(soc_name__isnull=False)),
            mild=Count('ctcae_grade', filter=Q(ctcae_grade='mild')),
            moderate=Count('ctcae_grade', filter=Q(ctcae_grade='moderate')),
            severe=Count('ctcae_grade', filter=Q(ctcae_grade='severe')),
            life_threatening=Count('ctcae_grade', filter=Q(ctcae_grade='life_threatening')),
            fatal=Count('ctcae_grade', filter=Q(ctcae_grade='fatal')),

        )

        overral_hlt = self.ae_record_cls.objects.filter(q).values('soc_name', 'hlt_name').annotate(
            total=Count('hlt_name', filter=Q(soc_name__isnull=False)),
            mild=Count('ctcae_grade', filter=Q(ctcae_grade='mild')),
            moderate=Count('ctcae_grade', filter=Q(ctcae_grade='moderate')),
            severe=Count('ctcae_grade', filter=Q(ctcae_grade='severe')),
            life_threatening=Count('ctcae_grade', filter=Q(ctcae_grade='life_threatening')),
            fatal=Count('ctcae_grade', filter=Q(ctcae_grade='fatal')),
        )

        overall = []
        unique_soc = []
        for hlt in overral_hlt:
            soc_name = hlt.get('soc_name')
            soc_stats = next((sub for sub in overral_soc if sub['soc_name'] == soc_name), None)
            if soc_stats and soc_stats.get('hlt') is not None:
                del hlt['soc_name']
                soc_stats['hlt'].append(hlt)
            elif soc_stats:
                del hlt['soc_name']
                soc_stats['hlt'] = [hlt]
            if soc_name not in unique_soc:
                overall.append(soc_stats)
                unique_soc.append(soc_name)

        return overall

    @property
    def sae_hiv_uninfected(self):
        return self.adverse_events_by_hiv_status(status=NEG)

    @property
    def sae_hiv_infected(self):
        return self.adverse_events_by_hiv_status(status=POS)

    @property
    def sae_received_first_dose(self):
        return self.adverse_event_by_vaccination(dose='first_dose')

    @property
    def sae_received_second_dose(self):
        return self.adverse_event_by_vaccination(dose='second_dose')

    @property
    def sae_related_ip(self):
        return self.adverse_event_by_attrib(choice=YES)

    @property
    def sae_not_related_ip(self):
        return self.adverse_event_by_attrib(choice=NO)

    @property
    def sae_received_first_dose_plus_28(self):
        pass

    @property
    def new_sae_listing(self):
        sae_ids = self.sae_record_cls.objects.all().order_by('-date_aware_of')[0:3].values_list(
            'serious_adverse_event__subject_visit__subject_identifier', flat=True)
        all_sae = []
        count = 0
        for subject_identifier in sae_ids:
            count += 1
            sae = self.sae_record(subject_identifier)
            ae = self.ae_record(subject_identifier)
            consent = self.consent(subject_identifier)
            hiv_test = self.hiv_test(subject_identifier)
            demographics = self.demographics_record(subject_identifier)

            first_dose_vaccine = self.vaccination_record(
                subject_identifier=subject_identifier, dose='first_dose')

            second_dose_vaccine = self.vaccination_record(
                subject_identifier=subject_identifier, dose='second_dose')

            all_sae.append((subject_identifier, sae, ae, count, consent,
                            first_dose_vaccine, second_dose_vaccine,
                            demographics, hiv_test))
        return all_sae

    @property
    def all_sae_records(self):
        sae_ids = self.sae_record_cls.objects.all().values_list(
            'serious_adverse_event__subject_visit__subject_identifier', flat=True)
        all_sae = []
        for subject_identifier in sae_ids:
            sae = self.sae_record(subject_identifier)
            ae = self.ae_record(subject_identifier)
            consent = self.consent(subject_identifier)
            hiv_test = self.hiv_test(subject_identifier)
            demographics = self.demographics_record(subject_identifier)

            first_dose_vaccine = self.vaccination_record(
                subject_identifier=subject_identifier, dose='first_dose')

            second_dose_vaccine = self.vaccination_record(
                subject_identifier=subject_identifier, dose='second_dose')

            all_sae.append((subject_identifier, sae, ae, consent,
                            first_dose_vaccine, second_dose_vaccine,
                            demographics, hiv_test))
        return all_sae

    def adverse_events_by_hiv_status(self, status=None):
        hiv_test = self.rapid_hiv_testing_cls.objects.filter(
            Q(hiv_result=status) | Q(rapid_test_result=status)).values_list(
                'subject_visit__subject_identifier', flat=True).distinct()

        q = Q(adverse_event__subject_visit__subject_identifier__in=hiv_test)

        overall = self.overral_filter_by_query_object(q)
        return overall

    def adverse_event_by_attrib(self, choice):
        q = Q(ae_rel=choice)
        overall = self.overral_filter_by_query_object(q)
        return overall

    def adverse_event_by_vaccination(self, dose):
        received_dose = self.vaccination_detail_cls.objects.filter(
            received_dose_before=dose).values_list(
            'subject_visit__subject_identifier', flat=True).distinct()
        q = Q(adverse_event__subject_visit__subject_identifier__in=received_dose)
        overall = self.overral_filter_by_query_object(q)
        return overall

    def overral_filter_by_query_object(self, query):
        soc_list = self.ae_record_cls.objects.filter(query).values('soc_name').annotate(
            total=Count('soc_name', filter=Q(soc_name__isnull=False)),
            mild=Count('ctcae_grade', filter=Q(ctcae_grade='mild')),
            moderate=Count('ctcae_grade', filter=Q(ctcae_grade='moderate')),
            severe=Count('ctcae_grade', filter=Q(ctcae_grade='severe')),
            life_threatening=Count('ctcae_grade', filter=Q(ctcae_grade='life_threatening')),
            fatal=Count('ctcae_grade', filter=Q(ctcae_grade='fatal')),
        )

        hlt_list = self.ae_record_cls.objects.filter(query).values(
            'soc_name', 'hlt_name').annotate(
            total=Count('hlt_name', filter=Q(hlt_name__isnull=False)),
            mild=Count('ctcae_grade', filter=Q(ctcae_grade='mild')),
            moderate=Count('ctcae_grade', filter=Q(ctcae_grade='moderate')),
            severe=Count('ctcae_grade', filter=Q(ctcae_grade='severe')),
            life_threatening=Count('ctcae_grade', filter=Q(ctcae_grade='life_threatening')),
            fatal=Count('ctcae_grade', filter=Q(ctcae_grade='fatal')),
        )

        overall = []
        unique_soc = []
        for hlt in hlt_list:
            soc_name = hlt.get('soc_name')
            soc_stats = next((sub for sub in soc_list if sub['soc_name'] == soc_name), None)
            if soc_stats and soc_stats.get('hlt') is not None:
                del hlt['soc_name']
                soc_stats['hlt'].append(hlt)
            elif soc_stats:
                del hlt['soc_name']
                soc_stats['hlt'] = [hlt]
            if soc_name.lower() not in unique_soc:
                overall.append(soc_stats)
                unique_soc.append(soc_name.lower())

        return overall

    def hiv_test(self, subject_identifier):
        try:
            return self.rapid_hiv_testing_cls.objects.get(
                subject_visit__subject_identifier=subject_identifier,)
        except self.rapid_hiv_testing_cls.DoesNotExist:
                pass
        return None

    def consent(self, subject_identifier):
        try:
            return self.consent_cls.objects.get(subject_identifier=subject_identifier)
        except self.consent_cls.DoesNotExist:
                pass
        return None

    def sae_record(self, subject_identifier):
        try:
            return self.sae_record_cls.objects.get(
                serious_adverse_event__subject_visit__subject_identifier=subject_identifier)
        except self.sae_record_cls.DoesNotExist:
                pass
        return None

    def ae_record(self, subject_identifier):
        try:
            return self.ae_record_cls.objects.get(
                adverse_event__subject_visit__subject_identifier=subject_identifier)
        except self.ae_record_cls.DoesNotExist:
                pass
        return None

    def vaccination_record(self, subject_identifier, dose):
        try:
            return self.vaccination_detail_cls.objects.get(
                subject_visit__subject_identifier=subject_identifier,
                received_dose_before=dose)
        except self.vaccination_detail_cls.DoesNotExist:
                pass
        return None

    def demographics_record(self, subject_identifier):
        try:
            return self.demographics_data_cls.objects.get(
                subject_visit__subject_identifier=subject_identifier)
        except self.demographics_data_cls.DoesNotExist:
                pass
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            new_sae_listing=self.new_sae_listing,
            # all_sae_records=self.all_sae_records,
            sae_overral_adverse_events=self.sae_overral_adverse_events,
            sae_hiv_uninfected=self.sae_hiv_uninfected,
            sae_hiv_infected=self.sae_hiv_infected,
            sae_received_first_dose=self.sae_received_first_dose,
            sae_received_second_dose=self.sae_received_second_dose,
            sae_related_ip=self.sae_related_ip,
            sae_not_related_ip=self.sae_not_related_ip,
            sae_received_first_dose_plus_28=self.sae_received_first_dose_plus_28
            )
        return context

