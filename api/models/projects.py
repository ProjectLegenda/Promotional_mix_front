from django.db import models
from .group import group

# projects model use to control projects level operation & data
class projects(models.Model):
    project_name = models.CharField(max_length=255, unique=True)
    project_status = models.CharField(max_length=30) # tbd:项目的状态有以下枚举值 ["EMPTY","MODELING","SIMULATION"]
    mcmc_current_task_id = models.CharField(max_length=100, null=True)
    simulation_current_task_id = models.CharField(max_length=100, null=True)
    simulations_list=models.CharField(max_length=500, null=True) #tbd
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    delete_datetime = models.DateTimeField(null=True)
    delete_flag = models.BooleanField(null=True)
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    project_privileges=models.CharField(max_length=500) #tbd