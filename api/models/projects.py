from django.db import models
from .group import group
from .role import role

class projects(models.Model):
    
    pk = models.CompositePrimaryKey("group_id", "project_name")
    project_name = models.CharField(max_length=255)
    project_status = models.CharField(max_length=30) # 枚举值tbd ["EMPTY","MODEL_RUNNING","MODEL","OUTPUT","SIMULATION_RUNNING""SIMULATION"]
    mcmc_current_task_id = models.CharField(max_length=100, null=True)
    simulation_current_task_id = models.CharField(max_length=100, null=True)
    simulations_list=models.CharField(max_length=500, null=True) #tbd
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    delete_datetime = models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=0)
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    is_publish= models.BooleanField(default=0) 
    role=models.ForeignKey(role, on_delete=models.CASCADE)