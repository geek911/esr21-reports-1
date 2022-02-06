from django.apps import apps as django_apps
from django.db.models import Q, Count
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import NEG, POS, YES, NO


class AdverseEventRecordViewMixin(EdcBaseViewMixin):
    ae_record_model = 'esr21_subject.adverseeventrecord'
    rapid_hiv_testing_model = 'esr21_subject.rapidhivtesting'
    vaccination_detail_model = 'esr21_subject.vaccinationdetails'

    @property
    def ae_record_cls(self):
        return django_apps.get_model(self.ae_record_model)

    @property
    def vaccination_detail_cls(self):
        return django_apps.get_model(self.vaccination_detail_model)

    @property
    def rapid_hiv_testing_cls(self):
        return django_apps.get_model(self.rapid_hiv_testing_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            overral_adverse_events=self.overral_adverse_events
        )
        return context

    @property
    def overral_adverse_events(self):
        overral_soc = self.ae_record_cls.objects.values('soc_name').annotate(
            total=Count('soc_name', filter=Q(soc_name__isnull=False)),
            mild=Count('ctcae_grade', filter=Q(ctcae_grade='mild')),
            moderate=Count('ctcae_grade', filter=Q(ctcae_grade='moderate')),
            severe=Count('ctcae_grade', filter=Q(ctcae_grade='severe')),
            life_threatening=Count('ctcae_grade', filter=Q(ctcae_grade='life_threatening')),
            fatal=Count('ctcae_grade', filter=Q(ctcae_grade='fatal')),

        )

        overral_hlt = self.ae_record_cls.objects.values('soc_name', 'hlt_name').annotate(
            total=Count('hlt_name', filter=Q(soc_name__isnull=False)),
            mild=Count('ctcae_grade', filter=Q(ctcae_grade='mild')),
            moderate=Count('ctcae_grade', filter=Q(ctcae_grade='moderate')),
            severe=Count('ctcae_grade', filter=Q(ctcae_grade='severe')),
            life_threatening=Count('ctcae_grade', filter=Q(ctcae_grade='life_threatening')),
            fatal=Count('ctcae_grade', filter=Q(ctcae_grade='fatal')),
        )

        overall = []
        for hlt in overral_hlt:
            soc_name = hlt.get('soc_name')
            soc_stats = next((sub for sub in overral_soc if sub['soc_name'] == soc_name), None)
            if soc_stats and soc_stats.get('hlt') is not None:
                del hlt['soc_name']
                soc_stats['hlt'].append(hlt)
            elif soc_stats:
                del hlt['soc_name']
                soc_stats['hlt'] = [hlt]
            overall.append(soc_stats)

    @property
    def hiv_uninfected(self):
        return self.adverse_events_by_hiv_status(NEG)

    @property
    def hiv_infected(self):
        return self.adverse_events_by_hiv_status(POS)

    @property
    def received_first_dose(self):
        return self.adverse_event_by_vaccination('first_dose')

    @property
    def received_second_dose(self):
        return self.adverse_event_by_vaccination('second_dose')

    @property
    def related_ip(self):
        return self.adverse_event_by_attrib(YES)

    @property
    def not_related_ip(self):
        return self.adverse_event_by_attrib(NO)

    @property
    def received_first_dose_plus_28(self):
        pass

    def adverse_events_by_hiv_status(self, status=None):
        hiv_test = self.rapid_hiv_testing_cls.objects.filter(
            Q(hiv_result=status) | Q(rapid_test_result=status)).values_list(
                'subject_visit__subject_identifier', flat=True).distinct()

        q = Q(adverse_event__subject_visit__subject_identifier__in=hiv_test)

        overall = self.overral_filter_by_query_object(q)
        return overall

    @property
    def adverse_event_by_attrib(self, attrib):
        q = Q(ae_rel=attrib)
        overall = self.overral_filter_by_query_object(q)
        return overall

    @property
    def adverse_event_by_vaccination(self, dose):
        received_dose = self.vaccination_detail_cls.objects.filter(
            received_dose_before=dose).values_list(
            'subject_visit__subject_identifier', flat=True).distinct()
        q = Q(adverse_event__subject_visit__subject_identifier__in=received_dose)
        overall = self.overral_filter_by_query_object(q)
        return overall

    @property
    def overral_filter_by_query_object(self, q):
        soc_list = self.ae_record_cls.objects.filter(q).values('soc_name').annotate(
            total=Count('soc_name', filter=Q(soc_name__isnull=False)),
            mild=Count('ctcae_grade', filter=Q(ctcae_grade='mild')),
            moderate=Count('ctcae_grade', filter=Q(ctcae_grade='moderate')),
            severe=Count('ctcae_grade', filter=Q(ctcae_grade='severe')),
            life_threatening=Count('ctcae_grade', filter=Q(ctcae_grade='life_threatening')),
            fatal=Count('ctcae_grade', filter=Q(ctcae_grade='fatal')),
        )

        hlt_list = self.ae_record_cls.objects.filter(q).values(
            'soc_name', 'hlt_name').annotate(
            total=Count('hlt_name', filter=Q(hlt_name__isnull=False)),
            mild=Count('ctcae_grade', filter=Q(ctcae_grade='mild')),
            moderate=Count('ctcae_grade', filter=Q(ctcae_grade='moderate')),
            severe=Count('ctcae_grade', filter=Q(ctcae_grade='severe')),
            life_threatening=Count('ctcae_grade', filter=Q(ctcae_grade='life_threatening')),
            fatal=Count('ctcae_grade', filter=Q(ctcae_grade='fatal')),
        )

        overall = []
        for hlt in hlt_list:
            soc_name = hlt.get('soc_name')
            soc_stats = next((sub for sub in soc_list if sub['soc_name'] == soc_name), None)
            if soc_stats and soc_stats.get('hlt') is not None:
                del hlt['soc_name']
                soc_stats['hlt'].append(hlt)
            elif soc_stats:
                del hlt['soc_name']
                soc_stats['hlt'] = [hlt]
            overall.append(soc_stats)

        return overall

