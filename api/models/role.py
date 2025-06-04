from django.db import models
from django.contrib.auth.models import User

class role(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(null=True) #tbd
    ROLE_CHOICES = [
        (1, 'Guest'),  
        (2, 'Maintainer'),
        (3, 'Owner')
    ]
    role=models.IntegerField(choices=ROLE_CHOICES,default=1)   # 枚举值 ["Guest","Maintainer","Owner"]
    created_datetime= models.DateTimeField(auto_now_add=True)
    updated_datetime= models.DateTimeField(auto_now=True)
    delete_datetime = models.DateTimeField(null=True)
    is_active=models.BooleanField(default=1)
    roleoptions=models.CharField(null=True)
    activity=models.CharField(null=True)

