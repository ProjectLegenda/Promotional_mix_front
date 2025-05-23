from django.db import models

class group(models.Model):
    group_name = models.CharField(max_length=255, unique=True,primary_key=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    delete_datetime = models.DateTimeField(null=True)
    delete_flag = models.BooleanField(null=True)
    project_count=  models.IntegerField(default=0) #tbd
    group_privileges=models.CharField(max_length=500)  #tbd md update column name rename
