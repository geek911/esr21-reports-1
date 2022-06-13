from django.db import models
import json
from ..choices import STATISTICS_TYPE

class DashboardStatistics(models.Model):
    type = models.CharField(max_length=20, choices=STATISTICS_TYPE)
    variable = models.CharField(max_length=20, ) # name of the values stored in an array
    values  = models.CharField(max_length=255) # values in json array in text (e.g "[4,4,5,3,5,6]" )
    
    @property
    def overall(self):
        
        values = json.loads(self.values)
        
        return 0