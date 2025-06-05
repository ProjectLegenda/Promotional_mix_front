from django.db import models

class df_mccp(models.Model):
        yyyymm       =models.IntegerField()
        brand_en =models.CharField(max_length=500)
        f2f    =models.FloatField()
        ht     =models.FloatField()
        iengage=models.FloatField()
        ratio =models.FloatField()