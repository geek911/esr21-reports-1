from django.core.management.base import BaseCommand

from ...classes import  QueryGeneration


class Command(BaseCommand):

    help = 'Generate queries'

    def handle(self, *args, **kwargs):
        queries = QueryGeneration()
        print("Generating queries for missing first dose")
        queries.first_dose_second_dose_missing
        print("Generating queries for vaccinated but not eligible participants")
        queries.ineligible_vaccinated_participant
        print("Generating quesries for male with child bearing potential")
        queries.male_child_bearing_potential
        print("Generating queries with ae date before vaccination")
        queries.ae_data_issues
        print("Generating queries for missing visit forms")
        queries.missing_visit_forms
        print('Done')



