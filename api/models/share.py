from django.db import models
from .projects import projects
from .role import role

class share(models.Model):

    pk = models.CompositePrimaryKey("role_id", "projects_id")
    role = models.ForeignKey(role, on_delete=models.CASCADE) 
    projects =models.ForeignKey(projects, on_delete=models.CASCADE)
    msg=models.CharField(null=True) 