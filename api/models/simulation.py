from django.db import models
from .projects import projects

class simulation(models.Model):

    pk_id=models.AutoField(primary_key=True)
    simulation_name= models.TextField()
    parameters= models.TextField()
    optimization_output = models.TextField()
    optimization_type=models.TextField()
    optimal_channel_performance=models.TextField()
    current_channel_performence=models.TextField()
    simulated_promotion_base=models.TextField()
    simulated_channel_contribution=models.TextField()
    simulated_roi_mroi=models.TextField()
    simulated_cost_dist=models.TextField()
    simulated_unit_price=models.TextField()
    last = models.BooleanField()
    projects = models.ForeignKey(projects, on_delete=models.CASCADE)
