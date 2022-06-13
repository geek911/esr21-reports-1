from django.db import models
from edc_search.model_mixins import SearchSlugManager
from edc_base.model_mixins import BaseUuidModel


class VaccinationStatisticsManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class VaccinationStatistics(BaseUuidModel):

    objects = VaccinationStatisticsManager()

    site = models.CharField(
        verbose_name='Site',
        max_length=150,
    )

    dose_1 = models.PositiveIntegerField(
        verbose_name='First Dose',
        default=0
    )

    dose_2 = models.PositiveIntegerField(
        verbose_name='Second Dose',
        default=0
    )

    dose_2 = models.PositiveIntegerField(
        verbose_name='Booster Dose',
        default=0
    )
