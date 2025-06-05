from api.models import group, projects
from django.http import JsonResponse
from django.db import  transaction
from datetime import datetime
from django.db.models import Count, Q
import json
from .exceptionhandler import exceptionhandler
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# privileges枚举值需要check，现在没有rename，UI界面上也没有
@exceptionhandler
@login_required
def get_groups(requet):
    current_user = request.user
    if current_user.is_authenticated: # same function with @login_required?
        r = current_user.role # due to One-to-One field
        if r.role == 3: # Owner
            groups_show = group.objects.all()
            result_group_list = []
            for g in groups_show:
                projects_show = projects.objects.filter(group__group_name=g.group_name)
                p_count = projects_show.count()
                result_project_list = []
                for p in projects_show:
                    p_result = {
                        "project_name": p.project_name,
                        "project_status": p.project_status,
                        "updated_datetime": p.updated_datetime,
                        "project_privileges": ["Publish","Enter","Copy","Share","Delete","Rename"]
                    }
                    result_project_list.append(p_result)
                g_result = {
                    "group_name": g.group_name,
                    "created_datetime": g.created_datetime,
                    "project_count": p_count,
                    "group_internal_privileges": ["Create New Analysis","Upload","Delete","Rename"],
                    "project_list": result_project_list
                }
                result_group_list.append(g_result)
            result_response = {
                "group_meta": {
                    "group_privileges": ["Create New Group"]
                },
                "group_list":[result_group_list]
            }
            return JsonResponse(result_response)
        elif r.role == 2: # Maintainer
            groups_show = group.objects.all()
            result_group_list = []
            for g in groups_show:
                projects_show = projects.objects.filter(group__group_name=g.group_name)
                p_count = projects_show.count()
                result_project_list = []
                for p in projects_show:
                    if p.role.auth_user == current_user: # 是当前用户创建的project
                        p_result = {
                            "project_name": p.project_name,
                            "project_status": p.project_status,
                            "updated_datetime": p.updated_datetime,
                            "project_privileges": ["Publish","Enter","Copy","Share","Delete","Rename"]
                        }
                    else: # 不是当前用户创建的project
                        p_result = {
                            "project_name": p.project_name,
                            "project_status": p.project_status,
                            "updated_datetime": p.updated_datetime,
                            "project_privileges": ["Enter","Copy","Share"]
                        }
                    result_project_list.append(p_result)
                if g.role.auth_user == current_user: # 是当前用户创建的group
                    g_result = {
                        "group_name": g.group_name,
                        "created_datetime": g.created_datetime,
                        "project_count": p_count,
                        "group_internal_privileges": ["Create New Analysis","Upload","Delete","Rename"],
                        "project_list": result_project_list
                    }
                else: # 不是当前用户创建的group
                    g_result = {
                        "group_name": g.group_name,
                        "created_datetime": g.created_datetime,
                        "project_count": p_count,
                        "group_internal_privileges": ["Create New Analysis", "Upload"],
                        "project_list": result_project_list
                    }
                result_group_list.append(g_result)
            result_response = {
                "group_meta": {
                    "group_privileges": ["Create New Group"]
                },
                "group_list":[result_group_list]
            }
            return JsonResponse(result_response)
        else: # Guest: groups with published or shared projects
            groups_w_published_projects = group.objects.filter(projects__is_publish=1).distinct()
            groups_w_shared_projects = groups.objects.filter(projects__share__role__auth_user=current_user).distinct()
            groups_show = groups_w_published_projects.union(groups_w_shared_projects).distinct()
            result_group_list = []
            for g in groups_show:
                projects_show = projects.objects.filter(Q(is_publish=True)|Q(share__role__auth_user=current_user), group__group_name=g.group_name).distinct()
                p_count = projects_show.count()
                result_project_list = []
                for p in projects_show:
                    p_result = {
                        "project_name": p.project_name,
                        "project_status": p.project_status,
                        "updated_datetime": p.updated_datetime,
                        "project_privileges": ["Enter"]
                    }
                    result_project_list.append(p_result)
                g_result = {
                    "group_name": g.group_name,
                    "created_datetime": g.created_datetime,
                    "project_count": p_count,
                    "group_internal_privileges": [],
                    "project_list": result_project_list
                }
                result_group_list.append(g_result)
            result_response = {
                "group_meta": {
                    "group_privileges": []
                },
                "group_list":[result_group_list]
            }
            return JsonResponse(result_response)
        
        
@exceptionhandler
@login_required
def group_add_or_delete(request,group_name):
    current_user = request.user
    if current_user.is_authenticated: # same function with @login_required?
        r = current_user.role # due to One-to-One field
        permission = r.role
        if request.method == "PUT":
            return addgrp(request, group_name, permission)
        elif request.method == 'DELETE':
            return deletegrp(request, group_name, permission)


# Add group: PUT 可以把参数放url里？还是在request.body里？不需要handle空group name？
@transaction.atomic      
def addgrp(request, group_name, permission):
    # if request.method == "PUT":
    #     group_name = json.loads(request.body).get("group_name")
    #     # if not group_name:
    #     #     return JsonResponse({"status": 0, "message": "Group name is required."})
    if permission == 3 or permission == 2: # Owner or Maintainer can create new groups
        new_group, created = group.objects.select_for_update().get_or_create(group_name=group_name)
        if created:
            return JsonResponse({"status": 1})
        else:
            return JsonResponse({"status": 0, "message": "Group name has been used. Please rename."})
    else: # Guest
        return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
    

# 真delete
@transaction.atomic
def deletegrp(request, group_name, permission):
    if permission == 3: # Owner can delete any group
        pass
    elif permisison == 2: # Maintainer can only delete groups created by him/her
        if g.role.auth_user != request.user: # 不是当前用户创建的group
            return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
    else: # Guest
        return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
    
    try:
        g = group.objects.select_for_update().get(group_name=group_name)
        g.delete() # will delete all projects in the group due to on_delete=models.CASCADE
        return JsonResponse({'status': 1})
    except group.DoesNotExist:
        return JsonResponse({'status': 0, "message": "Group not found."}) # msg TBD
    

# different url with add/delete group
@exceptionhandler
@transaction.atomic
@login_required
def renamegrp(request, group_name):
    current_user = request.user
    if current_user.is_authenticated: # same function with @login_required?
        r = current_user.role # due to One-to-One field
        permission = r.role
        
        if permission == 3: # Owner can rename any group
            pass
        elif permisison == 2: # Maintainer can only rename groups created by him/her
            if g.role.auth_user != current_user: # 不是当前用户创建的group
                return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
        else: # Guest
            return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
        
        data = json.loads(request.body)
        group_name_new = data.get("group_name_new") # param name to be confirmed
        if not group_name_new:
            return JsonResponse({'status': 0, "message": "Missing new group name."}) # msg TBD
        if group.objects.filter(group_name=group_name_new).exists():
            return JsonResponse({'status': 0, "message": "New group name already exists."}) # msg TBD
        
        try:
            g = group.objects.select_for_update().get(group_name = group_name)
            # rename
            g.group_name = group_name_new
            g.save() # auto_now only works when calling Model.save()
            return JsonResponse({'status': 1})
        except group.DoesNotExist:
            return JsonResponse({'status': 0, "message": "Original group not found."}) # msg TBD
        
        
        
        
        
            
    
    


