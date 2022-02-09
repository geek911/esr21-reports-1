
from django.apps import apps as django_apps
from django.db.models import Q

class ScreeningReportsViewMixin:
    
    eligibility_model = 'esr21_subject.eligibilityconfirmation'
    consent_model = 'esr21_subject.informedconsent'
    
    
    @property
    def eligibility_model_cls(self):
        return django_apps.get_model(self.eligibility_model)
    
    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.consent_model)
    
    
    @property
    def total_screened_participants(self):
        overall = self.eligibility_model_cls.objects.all().count()
        gaborone = self.eligibility_model_cls.objects.filter(site__id='40').count()
        maun = self.eligibility_model_cls.objects.filter(site__id='41').count()
        serowe = self.eligibility_model_cls.objects.filter(site__id='42').count()
        f_town = self.eligibility_model_cls.objects.filter(site__id='43').count()
        phikwe = self.eligibility_model_cls.objects.filter(site__id='44').count()
        
        import pdb; pdb.set_trace()
        return [overall,gaborone,maun,serowe,f_town,phikwe]
    
    @property
    def enrolled_participants(self):
        eligible_identifier = self.eligibility_model_cls.filter(is_eligible=True).values_list('screening_identifier', flat=True)
        eligible_identifier = list(set(eligible_identifier))
        
        consent_screening_ids = self.eligibility_model_cls.objects.all().values_list('screening_identifier', flat=True)
        consent_screening_ids = list(set(consent_screening_ids))
        no_consent_screenigs = list(set(eligible_identifier) - set(consent_screening_ids))
        
        total_screened = self.eligibility_model_cls.objects.filter(~Q(screening_identifier__in=no_consent_screenigs))

        return total_screened
    
    @property
    def screening_failure(self):
        pass
    
    @property
    def screening_failure_reasons(self):
        pass