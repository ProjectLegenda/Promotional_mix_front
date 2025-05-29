from django.db import models
from .projects import projects

class rawdata(models.Model):
    
    df_rawdata = models.TextField()
    df_data_ab_others== models.TextField()
    brand_name= models.CharField()
    time_period_id= models.CharField()
    data_version_id= models.CharField()
    ori_channel_list models.TextField()
    ori_channel_prior= models.TextField()
    ori_segment= models.TextField()
    last = models.BooleanField(default=1)
    projects = models.ForeignKey(projects, on_delete=models.CASCADE)



