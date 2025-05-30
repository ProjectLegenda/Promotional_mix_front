from django.contrib import admin
from api.models import role,group, projects,share,rawdata,mmm,simulation

# Register your models here.
myModels = [role,group, projects,share,rawdata,mmm,simulation]  # iterable list
admin.site.register(myModels)

# admin.site.register(role)
# admin.site.register(group)
# admin.site.register(projects)
# admin.site.register(share)
# admin.site.register(rawdata)
# admin.site.register(mmm)
# admin.site.register(simulation)
