from django.db import models
from .projects import projects

class rawdata(models.Model):
    
    df_rawdata = models.TextField()
    df_data_abothers== models.TextField()
    brand_name= models.TextField()
    time_period_id= models.TextField()
    data_version_id= models.TextField()
    ori_channel_list models.TextField()
    ori_channel_prior= models.TextField()
    ori_segment= models.TextField()
    last = models.BooleanField()
    projects = models.ForeignKey(projects, on_delete=models.CASCADE)



