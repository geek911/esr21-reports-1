
from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from django.contrib.sites.models import Site
from django.db.models import Q
import statistics
import numpy as np
import pandas as pd
from django_pandas.io import read_frame

class AgeDistributionGraphMixin(EdcBaseViewMixin):

    subject_screening_model = 'esr21_subject.eligibilityconfirmation'
    vaccination_model =  'esr21_subject.vaccinationdetails'
    consent_model = 'esr21_subject.informedconsent'
    site_outliers = []
    
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
            name =  site.name.split('-')[1]
            site_lists.append(name)
        return site_lists

    def site_index_mapping(self,site_name):
        return self.sites_names.index(site_name)
    
    @property
    def site_age_dist(self):
        age_dist = []
        for site in self.sites_names:
            age_dist.append([site,self.get_distribution_site(site_name_postfix=site)])
        return age_dist
    
    def age(self, enrolment_date=None, dob=None):
        age = enrolment_date.year - dob.year - ((enrolment_date.month, enrolment_date.day) < (dob.month, dob.day))
        return age
    
    def get_distribution_site(self, site_name_postfix):
        site_id = self.get_site_id(site_name_postfix)

        if site_id:
            vaccination_qs = self.vaccination_model_cls.objects.filter(
                Q(received_dose_before='first_dose') 
                )
            df_vaccination = read_frame(vaccination_qs,fieldnames=['subject_visit__subject_identifier','vaccination_date'])

            # DataFrames
            vaccination_identifiers = self.vaccination_model_cls.objects.filter( 
                Q(received_dose_before='first_dose')).values_list('subject_visit__subject_identifier', flat=True)
            vaccination_identifiers = list(set(vaccination_identifiers))

            consents = self.consent_model_cls.objects.filter(
                subject_identifier__in=vaccination_identifiers, 
                site_id=site_id)

            df_vaccination = df_vaccination.rename(columns={'subject_visit__subject_identifier': 'subject_identifier'})
            df_consent = read_frame(consents, fieldnames=['subject_identifier','dob'])
            df_vaccination = df_vaccination.drop_duplicates(subset="subject_identifier")

            merged_result = pd.merge(df_vaccination, df_consent, on='subject_identifier') 
           
            merged_result['Age'] = merged_result.apply(lambda x: self.age(x['vaccination_date'], x['dob']), axis=1)
            
            site_ages = merged_result['Age'].to_list()
            
            lowerquartile = np.quantile(site_ages, .25)
            median = statistics.median(site_ages)
            upperquartile = np.quantile(site_ages, .75)
           

            IQR = upperquartile - lowerquartile
            max_outlier = upperquartile+(1.5 * IQR)
            min_outlier = lowerquartile-(1.5 * IQR)

            # # outliers
            # IQR = upperquartile - lowerquartile
            # upper_outlier = upperquartile+(1.5 * IQR)
            # lower_outlier = lowerquartile-(1.5 * IQR)

            min_ages = []
            max_ages = []
            site_index = self.site_index_mapping(site_name_postfix)
            for age in site_ages:
                if age < max_outlier:
                    min_ages.append(age)
                else:
                    self.site_outliers.append([site_index,age])
                if age > min_outlier:
                    max_ages.append(age)
                else:
                    self.site_outliers.append([site_index,age])

            min = np.min(max_ages)
            max = np.max(min_ages)
            return [min,lowerquartile,median,upperquartile,max]

    def get_site_id(self, site_name_postfix):
        try:
            return Site.objects.get(name__endswith=site_name_postfix).id
        except Site.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            site_age_dist=self.site_age_dist,
            site_outliers=self.site_outliers
        )
        return context
