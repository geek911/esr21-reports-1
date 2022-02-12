
import imp


import json
from edc_base.view_mixins import EdcBaseViewMixin
from esr21_subject.models import VaccinationDetails, InformedConsent
from edc_constants.constants import FEMALE, MALE
class EnrollmentGraphMixin(EdcBaseViewMixin):

	@property
	def site_ids(self):
		return [40, 41, 42, 43, 44]


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
			percentages.append(perc)
		return percentages
		


	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		gender_by_site = self.get_vaccinated_by_site()
		overall_participant = self.get_overall_participant()
		overall_percentages = self.get_overall_percentage()

		print(overall_participant)


		context.update(
			females=json.dumps(gender_by_site['females']),
			males=json.dumps(gender_by_site['males']),
			overall = json.dumps(overall_participant),
			overall_percentages=json.dumps(overall_percentages)
		)

		return context





	# def get_context_data(self, **kwargs):
    # 	context = super().get_context_data(**kwargs)

	# 	context.update(
    #         test='guuutuutg'
	# 	)

	# 	return context


"""
		$(document).ready(function(){
        	var ctx = document.getElementById('myChart').getContext('2d');
        	var myChart = new Chart(ctx, {
            	type: 'doughnut',
				data: {
					labels: [1,2,3,4,5], //loop through queryset, 
					datasets: [{
						label: '# of users',
						data: [1,2,3,4,5],
						backgroundColor: [
							'rgba(255, 99, 132, 0.2)', 
							'rgba(54, 162, 235, 0.2)',
							'rgba(255, 206, 86, 0.2)',
							'rgba(75, 192, 192, 0.2)',
							'rgba(153, 102, 255, 0.2)',
							'rgba(255, 159, 64, 0.2)'
						],
						borderColor: [
							'rgba(255, 99, 132, 1)',
							'rgba(54, 162, 235, 1)',
							'rgba(255, 206, 86, 1)',
							'rgba(75, 192, 192, 1)',
							'rgba(153, 102, 255, 1)',
							'rgba(255, 159, 64, 1)'
						],
						borderWidth: 1
					}]
				},
				options: {
					scales: {
						y: {
							beginAtZero: true
						}
					}
				}
			});
    	});

"""
