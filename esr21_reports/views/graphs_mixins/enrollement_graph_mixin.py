import json
from django.contrib.sites.models import Site
from edc_base.view_mixins import EdcBaseViewMixin
from esr21_subject.models import VaccinationDetails, InformedConsent
from edc_constants.constants import FEMALE, MALE
class EnrollmentGraphMixin(EdcBaseViewMixin):
	
	
	@property
	def sites_names(self):
		site_lists = []
		sites = Site.objects.all()
		for site in sites:
			name =  site.name.split('-')[1]
			site_lists.append(name)
		return site_lists

	@property
	def site_age_dist(self):
		age_dist = []
		for site in self.sites_names:
			age_dist.append([site,self.get_distribution_site(site_name_postfix=site)])
		return age_dist

	@property
	def site_ids(self):
		site_ids = Site.objects.order_by('id').values_list('id', flat=True)
		return site_ids


	def get_vaccinated_by_site(self):
		statistics = {
			'females': [],
			'males': []}

		female_pids = InformedConsent.objects.filter(gender=FEMALE).values_list(
			'subject_identifier').distinct()

		male_pids = InformedConsent.objects.filter(gender=MALE).values_list(
			'subject_identifier').distinct()

		for site_id in self.site_ids:
			
			males = VaccinationDetails.objects.filter(
				subject_visit__subject_identifier__in=male_pids, received_dose_before='first_dose', site_id=site_id).count()
			statistics['males'].append(males)

			females = VaccinationDetails.objects.filter(
				subject_visit__subject_identifier__in=female_pids, received_dose_before='first_dose', site_id=site_id).count()
			statistics['females'].append(females)
		
		return statistics

	def get_overall_participant(self):
		overall_statistics = []
		
		for site_id in self.site_ids:

			enrolled = VaccinationDetails.objects.filter(
				received_dose_before='first_dose', site_id=site_id).values_list('subject_visit__subject_identifier').count()
			overall_statistics.append(enrolled)

		all_enrolled = VaccinationDetails.objects.filter(
			received_dose_before='first_dose').values_list('subject_visit__subject_identifier').count()

		overall_statistics.append(all_enrolled)


		return overall_statistics
			
	def get_overall_percentage(self):
		percentages = []
		total_participants = self.get_overall_participant()[-1]

		for participants in self.get_overall_participant():
			perc = (participants / total_participants) * 100
			percentages.append(round(perc, 1))
		return percentages
		


	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		gender_by_site = self.get_vaccinated_by_site()
		overall_participant = self.get_overall_participant()
		overall_percentages = self.get_overall_percentage()
		context.update(
			females=json.dumps(gender_by_site['females']),
			males=json.dumps(gender_by_site['males']),
			overall = json.dumps(overall_participant),
			overall_percentages=json.dumps(overall_percentages),
		)

		return context
