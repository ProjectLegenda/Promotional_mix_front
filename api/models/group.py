from django.db import models
from .role import role

class group(models.Model):
    
    group_name = models.CharField(max_length=255, primary_key=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    delete_datetime = models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=0)
    project_count=  models.IntegerField(default=0) 
    role=models.ForeignKey(role, on_delete=models.CASCADE) 
