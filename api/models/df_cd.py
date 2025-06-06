from django.db import models

class df_cd(models.Model):
        data_version_id =models.IntegerField()
        channel        =models.CharField(max_length=250)
        impact_factor     =models.FloatField()