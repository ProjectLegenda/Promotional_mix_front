from django.urls import path, re_path

from . import views

urlpatterns = [
      # path('test', views.test),
    # path('groups/<str:group_name>', views.v_group, name='v_group'),
    path('groups/', views.get_groups, name='get_groups'),
    path('groups/<str:group_name>/', views.group_add_or_delete, name='group_add_or_delete'),
    path('groups/<str:group_name>/rename/', views.renamegrp, name='renamegrp'),
   
    path('<str:group_name>/projects', views.get_projects, name='get_projects'),
    path('projects/<str:group_name>/<str:project_name>', views.project_add_or_delete, name='project_add_or_delete'),
   
    path('login/', views.v_login, name='login')
]
