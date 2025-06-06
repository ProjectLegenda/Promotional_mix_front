from django.db import models
from .projects import projects

class rawdata(models.Model):
    
    df_rawdata = models.TextField()
    df_data_ab_others= models.TextField(null=True) #formal change：null=False
    df_mccp= models.TextField(null=True)#formal change：null=False
    brand_name= models.CharField()
    yyyymm_end= models.IntegerField()
    data_version_id= models.IntegerField()
    ori_channel_list= models.TextField(default={
    "f2f": 0,
    "ht": 1,
    "digital_gsk": 2,
    "digital_third": 3,
    "standalone_online": 4,
    "collaboration_online": 5,
    "standalone_offline": 6,
    "collaboration_offline": 7,
    "sponsor": 8
    }
)
    ori_channel_prior= models.TextField()
    ori_segment= models.TextField(default={
    "segment_type_1": {
        "Total_market": 0,
        "Core": 1,
        "Engine": 2,
        "Others": 3
        },
    "segment_type_2": {
        "Total_market": 0,
        "Central": 1,
        "Regional": 2,
        "Others": 3
        },
    "segment_type_3": {
        "Total_market": 0,
        "Lupus_Center": 1, 
        "Others": 2
        },
    "segment_type_4": {
        "Total_market": 0,
        "Lupus_Certification_Center": 1,
        "Lupus_Demonstration_Center": 2,
        "Others": 3
        },
})
    last = models.BooleanField(default=1)
    projects = models.OneToOneField(projects, on_delete=models.CASCADE)