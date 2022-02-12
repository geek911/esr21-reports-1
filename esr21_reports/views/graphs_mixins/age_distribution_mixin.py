
from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from django.contrib.sites.models import Site
from django.db.models import Q
from datetime import datetime
import statistics
import numpy as np

class AgeDistributionGraphMixin(EdcBaseViewMixin):

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
    def site_age_dist(self):
        age_dist = [
            ['Gaborone', self.get_distribution_site(site_name_postfix='Gaborone',)],
            ['F/Town', self.get_distribution_site(site_name_postfix='Francistown')],
            ['S/Phikwe', self.get_distribution_site(site_name_postfix='Phikwe')],
            ['Maun', self.get_distribution_site(site_name_postfix='Maun')],
            ['Serowe', self.get_distribution_site(site_name_postfix='Serowe')]]

        return age_dist
    
    
    def get_distribution_site(self, site_name_postfix):
        
        
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
            
            passed_screening_ages = self.consent_model_cls.objects.filter(
                Q(subject_identifier__in=vaccination) & 
                Q(site_id=site_id)).values_list('dob')
                
            site_ages = []
            data = []
            for dob in passed_screening_ages:
                mask_date = ''.join(map(str,dob))
                mask_year = datetime.strptime(mask_date,'%Y-%m-%d')
                age = datetime.today().year - mask_year.year
                site_ages.append(age)    

            # calculate statistics
            #  [mean,lowerquartile,median,upperquartile,max]
            mean = statistics.mean(site_ages)
            lowerquartile = np.quantile(site_ages, .25)
            median = statistics.mean(site_ages)
            upperquartile = np.quantile(site_ages, .75)
            max = np.max(site_ages)
            data.append([mean,lowerquartile,median,upperquartile,max])
          
            return data
        
           
    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endswith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context.update(
            site_age_dist=self.site_age_dist,
        )
        return context
