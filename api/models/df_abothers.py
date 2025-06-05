from django.db import models

class df_abothers(models.Model):
        data_version_id =models.IntegerField()
        yyyymm          =models.IntegerField()
        brand_en        =models.CharField(max_length=500)
        f2f_total     =models.IntegerField()
        f2f_ab        =models.IntegerField()
        ht_total      =models.IntegerField()
        ht_ab         =models.IntegerField()