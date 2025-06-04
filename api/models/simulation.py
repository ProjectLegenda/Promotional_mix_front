from django.db import models
from .projects import projects

class simulation(models.Model):

    pk = models.CompositePrimaryKey("simulation_name", "projects_id")
    simulation_name= models.CharField()
    optimization_type=models.TextField()
    parameters= models.TextField(null=True)
    optimization_output = models.TextField(null=True)
    optimal_channel_performance=models.TextField(null=True)
    current_channel_performence=models.TextField(null=True)
    simulated_promotion_base=models.TextField(null=True)
    simulated_channel_contribution=models.TextField(null=True)
    simulated_roi_mroi=models.TextField(null=True)
    simulated_cost_dist=models.TextField(null=True)
    simulated_unit_price=models.TextField(null=True)
    last = models.BooleanField(default=1)
    projects = models.ForeignKey(projects, on_delete=models.CASCADE)
    is_visible=models.BooleanField(default=1)
    simulation_task_id = models.CharField(null=True)
    simulation_task_status = models.CharField( null=True)