
from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from django.contrib.sites.models import Site
from django.db.models import Q

class ScreeningGraphView(EdcBaseViewMixin):

    subject_screening_model = 'esr21_subject.eligibilityconfirmation'
    vaccination_model =  'esr21_subject.vaccinationdetails'
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
    def site_screenings(self):
        site_screenings = [
            ['Gaborone', self.get_screened_by_site(site_name_postfix='Gaborone',)],
            ['F/Town', self.get_screened_by_site(site_name_postfix='Francistown')],
            ['S/Phikwe', self.get_screened_by_site(site_name_postfix='Phikwe')],
            ['Maun', self.get_screened_by_site(site_name_postfix='Maun')],
            ['Serowe', self.get_screened_by_site(site_name_postfix='Serowe')]]

        return site_screenings
    
    
    def get_screened_by_site(self, site_name_postfix):
        
        
        
        
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            
            eligible_identifiers = self.subject_screening_cls.objects.filter(
                is_eligible=True).values_list('screening_identifier', flat=True)
            eligible_identifiers = list(set(eligible_identifiers))
            
            consent_screening_ids = self.subject_screening_cls.objects.all().values_list('screening_identifier', flat=True)
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
                Q(subject_identifier__in=vaccination) & 
                Q(site_id=site_id)).values_list('screening_identifier', flat=True)
                
            passed_screening = list(set(passed_screening))
            
            failed = total_screened.filter(~Q(screening_identifier__in=passed_screening) & Q(site_id=site_id)).count()
            
            total = len(passed_screening)+failed
            
            passed_screening = round(len(passed_screening)/total * 100,1)
            failed = round(failed/total * 100,1)

            return [passed_screening,failed]
        
    
    @property  
    def overall_screened(self):
            
            
            eligible_identifiers = self.subject_screening_cls.objects.filter(
                is_eligible=True).values_list('screening_identifier', flat=True)
            eligible_identifiers = list(set(eligible_identifiers))
            
            consent_screening_ids = self.subject_screening_cls.objects.all().values_list('screening_identifier', flat=True)
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
            
            failed = total_screened.filter(~Q(screening_identifier__in=passed_screening)).count()
            
            total = len(passed_screening)+failed
            
            passed_screening = round(len(passed_screening)/total * 100,1)
            failed = round(failed/total * 100,1)

            return [passed_screening,failed]
            
           
        
        
    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endswith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            site_screenings=self.site_screenings,
            overall_screened=self.overall_screened
        )
        return context
