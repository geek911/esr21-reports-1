from django.db import models
import json
from ..choices import STATISTICS_TYPE

class DashboardStatistics(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=500)
    