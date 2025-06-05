import json
# import pandas as pd
import io
from api.models import group, projects, rawdata
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.db import transaction
from .exceptionhandler import exceptionhandler
# from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required

# Simulation: where to get task_id and task_status?
@exceptionhandler
@login_required
def get_projects(request, group_name):
    current_user = request.user
    if current_user.is_authenticated: # same function with @login_required?
        r = current_user.role # due to One-to-One field
        if r.role == 3: # Owner
            projects_show = projects.objects.filter(group__group_name=group_name)
            result_project_list = []
            for p in projects_show:
                simulations_show = simulation.objects.filter(projects__project_name=p.project_name)
                result_simulation_list = list(simulations_show.values("simulation_name", "simulation_task_id", "is_visible", "simulation_task_status"))
                # result_simulation_list = []
                # for s in simulations_show:
                #     s_result = {
                #         "simulation_name": s.simulation_name,
                #         "task_id": s.task_id,
                #         "is_visible": s.is_visible,
                #         "task_status": s.task_status
                #     }
                #     result_simulation_list.append(s_result)
                p_result = {
                    "project_name": p.project_name,
                    "project_status": p.project_status,
                    "updated_datetime": p.updated_datetime,
                    "project_privileges": ["Publish","Enter","Copy","Share","Delete","Rename"],
                    "simulation_list": result_simulation_list
                }
                result_project_list.append(p_result)
            result_response = {
                "group_name": group_name,
                "project_list": [result_project_list]
            }
            return JsonResponse(result_response)
        elif r.role == 2: # Maintainer: show all projects but only visible simulations
            projects_show = projects.objects.filter(group__group_name=group_name)
            result_project_list = []
            for p in projects_show:
                if p.role.auth_user == current_user: # 是当前用户创建的project: all simulations
                    simulations_show = simulation.objects.filter(projects__project_name=p.project_name)
                    result_simulation_list = list(simulations_show.values("simulation_name", "simulation_task_id", "is_visible", "simulation_task_status"))
                    # result_simulation_list = []
                    # for s in simulations_show:
                    #     s_result = {
                    #         "simulation_name": s.simulation_name,
                    #         "task_id": s.task_id,
                    #         "is_visible": s.is_visible,
                    #         "task_status": s.task_status
                    #     }
                    #     result_simulation_list.append(s_result)
                    p_result = {
                        "project_name": p.project_name,
                        "project_status": p.project_status,
                        "updated_datetime": p.updated_datetime,
                        "project_privileges": ["Publish","Enter","Copy","Share","Delete","Rename"],
                        "simulation_list": result_simulation_list
                    }
                else: # 不是当前用户创建的project: 只能看到visible simulations
                    simulations_show = simulation.objects.filter(projects__project_name=p.project_name, is_visible=True)
                    result_simulation_list = list(simulations_show.values("simulation_name", "simulation_task_id", "is_visible", "simulation_task_status"))
                    p_result = {
                        "project_name": p.project_name,
                        "project_status": p.project_status,
                        "updated_datetime": p.updated_datetime,
                        "project_privileges": ["Enter","Copy","Share"],
                        "simulation_list": result_simulation_list
                    }
                result_project_list.append(p_result)
            result_response = {
                "group_name": group_name,
                "project_list": [result_project_list]
            }
            return JsonResponse(result_response)
        else: # Guest: published or shared projects and visible simulations
            projects_show = projects.objects.filter(Q(is_publish=True)|Q(share__role__auth_user=current_user), group__group_name=group_name).distinct()
            result_project_list = []
            for p in projects_show:
                simulations_show = simulation.objects.filter(projects__project_name=p.project_name, is_visible=True)
                result_simulation_list = list(simulations_show.values("simulation_name", "simulation_task_id", "is_visible", "simulation_task_status"))
                # result_simulation_list = []
                # for s in simulations_show:
                #     s_result = {
                #         "simulation_name": s.simulation_name,
                #         "task_id": s.task_id,
                #         # "is_visible": s.is_visible, # must be visible
                #         "task_status": s.task_status
                #     }
                #     result_simulation_list.append(s_result)
                p_result = {
                    "project_name": p.project_name,
                    "project_status": p.project_status,
                    "updated_datetime": p.updated_datetime,
                    "project_privileges": ["Enter"],
                    "simulation_list": result_simulation_list
                }
                result_project_list.append(p_result)
            result_response = {
                "group_name": group_name,
                "project_list": [result_project_list]
            }
            return JsonResponse(result_response)
        

@exceptionhandler
@login_required
def project_add_or_delete(request, group_name, project_name):
    current_user = request.user
    if current_user.is_authenticated: # same function with @login_required?
        r = current_user.role # due to One-to-One field
        permission = r.role
        if request.method == "PUT":
            return addproj(request, group_name, project_name, permission)
        elif request.method == 'DELETE':
            return deleteproj(request, group_name, project_name, permission)
        

@transaction.atomic
def addproj(request, group_name, project_name, permission):
    if permission == 3 or permission == 2: # Owner or Maintainer can create new projects
        data = json.loads(request.body)
        brand_name = data.get("brand_name")
        time_period_id = data.get("time_period_id")
        data_version_id = data.get("data_version_id")
        
        if not all([brand_name, time_period_id, data_version_id]):
            return JsonResponse({"status": 0, "message": "Missing parameters."}) # msg TBD
        
        try:
            target_group = group.objects.get(group_name=group_name)
        except group.DoesNotExist:
            return JsonResponse({"status": 0, "message": "Group not found."}) # msg TBD
            
        target_role = role.objects.get(auth_user=request.user)
        
        if projects.object.filter(project_name=project_name).exists():
            return JsonResponse({"status": 0, "message": "Project name has been used. Please rename."})
        
        new_project = projects.objects.select_for_update().create(
            project_name=project_name, 
            project_status="EMPTY",
            group=target_group,
            role=target_user)
        new_rawdata = rawdata.objects.select_for_update().create(
            brand_name=brand_name,
            time_period_id=time_period_id,
            data_version_id=data_version_id,
            projects=new_project
        )
    
        return JsonResponse({"status": 1})
    
    else: # Guest
        return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
    
    

# @transaction.atomic
# def deleteproj(request, group_name, project_name, permission):
#     if permission == 3: # Owner can delete any group
#         pass
#     elif permisison == 2: # Maintainer can only delete groups created by him/her
#         if g.role.auth_user != request.user: # 不是当前用户创建的group
#             return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
#     else: # Guest
#         return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
    
#     try:
#         p = projects.
    
    
# def deleteproj(request,group_name,project_name):
#     with transaction.atomic():
#         try:
#             pj_delete = projs.objects.select_for_update().get(project_name=project_name, group__group_name=group_name)
#             if pj_delete.project_status == "BAYES_MCMC_RUNNING":
#                 AsyncResult(pj_delete.mcmc_current_task_id).revoke(terminate=True)
#             pj_delete.delete()
#             return JsonResponse({'status': 1})
#         except projs.DoesNotExist:
#             return JsonResponse({'status': 0})
    

# # 真delete
# @transaction.atomic
# def deletegrp(request, group_name, permission):
#     if permission == 3: # Owner can delete any group
#         pass
#     elif permisison == 2: # Maintainer can only delete groups created by him/her
#         if g.role.auth_user != request.user: # 不是当前用户创建的group
#             return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
#     else: # Guest
#         return JsonResponse({"status": 0, "message": "No permission."}) # msg TBD
    
#     try:
#         g = group.objects.select_for_update().get(group_name=group_name)
#         g.delete() # will delete all projects in the group due to on_delete=models.CASCADE
#         return JsonResponse({'status': 1})
#     except group.DoesNotExist:
#         return JsonResponse({'status': 0, "message": "Group not found."}) # msg TBD
             
            


# @exceptionhandler
# def renameproj(request, group_name,project_name):
#     with transaction.atomic():
#         params = json.loads(request.body)
#         proj_nm_new = params['project_name_new']

#         try:
#             group.objects.select_for_update().get(group_name=group_name)
#         except group.DoesNotExist:
#             return JsonResponse({'status': 0,'message':'group_name is not correct'})
#         try:
#             proj_rename = projs.objects.select_for_update().get(project_name=project_name)
#         except group.DoesNotExist:
#             return JsonResponse({'status': 0,'message':'old project_name is not correct'})
#         proj_rename.project_name = proj_nm_new
#         proj_rename.save()
#         return JsonResponse({'status': 1})
# # @exceptionhandler
# def v_projects(request,group_name,project_name):
#     if request.method == "GET":
#        return exportproj(request, group_name,project_name)
#     if request.method == "PUT":
#         return addproj(request,group_name,project_name)
#     elif request.method == "DELETE":
#         return deleteproj(request,group_name,project_name)
#     elif request.method == "POST":
#         return importproj(request,group_name,project_name)



# def deleteproj(request,group_name,project_name):
#     with transaction.atomic():
#         try:
#             pj_delete = projs.objects.select_for_update().get(project_name=project_name, group__group_name=group_name)
#             if pj_delete.project_status == "BAYES_MCMC_RUNNING":
#                 AsyncResult(pj_delete.mcmc_current_task_id).revoke(terminate=True)
#             pj_delete.delete()
#             return JsonResponse({'status': 1})
#         except projs.DoesNotExist:
#             return JsonResponse({'status': 0})

# def exportproj(request, group_name,project_name):
#     with transaction.atomic():
#         request.params = request.GET
#         action = request.params['action']
#         # group_qs = group.objects.select_for_update().filter(group_name=group_name).values()
#         projects_qs = projs.objects.select_for_update().filter(project_name=project_name,group__group_name=group_name).values()
#         rawdata_qs = rawdata.objects.select_for_update().filter(projects__project_name=project_name).values()
#         handle_qs = handle.objects.select_for_update().filter(projects__project_name=project_name).values()
#         preprocessed_qs = preprocessed.objects.select_for_update().filter(projects__project_name=project_name).values()
#         baseline_qs = baseline.objects.select_for_update().filter(projects__project_name=project_name).values()
#         prior_mcmc_qs = prior_mcmc.objects.select_for_update().filter(projects__project_name=project_name).values()
#         bayes_mcmc_qs = bayes_mcmc.objects.select_for_update().filter(projects__project_name=project_name).values()
#         postprocess_qs = postprocess.objects.select_for_update().filter(projects__project_name=project_name).values()
#         aggregation_qs = aggregation.objects.select_for_update().filter(projects__project_name=project_name).values()
#         if action == 'export_excel':
#             # group_df = pd.DataFrame(list(group_qs))
#             projects_df = pd.DataFrame(list(projects_qs))
#             date_columns = projects_df.select_dtypes(include=['datetime64[ns, UTC]']).columns
#             for date_column in date_columns:
#                 projects_df[date_column] = projects_df[date_column].dt.tz_localize(None)
#             rawdata_df = pd.DataFrame(list(rawdata_qs))
#             handle_df = pd.DataFrame(list(handle_qs))
#             preprocessed_df = pd.DataFrame(list(preprocessed_qs))
#             baseline_df = pd.DataFrame(list(baseline_qs))
#             prior_mcmc_df = pd.DataFrame(list(prior_mcmc_qs))
#             bayes_mcmc_df = pd.DataFrame(list(bayes_mcmc_qs))
#             postprocess_df = pd.DataFrame(list(postprocess_qs))
#             aggregation_df = pd.DataFrame(list(aggregation_qs))
#             bio = io.BytesIO()
#             with pd.ExcelWriter(bio) as writer:
#                 # group_df.to_excel(writer, sheet_name="group", index=False)
#                 projects_df.to_excel(writer, sheet_name="projects", index=False)
#                 rawdata_df.to_excel(writer,sheet_name="rawdata", index=False)
#                 handle_df.to_excel(writer, sheet_name="handle", index=False)
#                 preprocessed_df.to_excel(writer, sheet_name="preprocessed", index=False)
#                 baseline_df.to_excel(writer, sheet_name="baseline", index=False)
#                 prior_mcmc_df.to_excel(writer, sheet_name="prior_mcmc", index=False)
#                 bayes_mcmc_df.to_excel(writer, sheet_name="bayes_mcmc", index=False)
#                 postprocess_df.to_excel(writer, sheet_name="postprocess", index=False)
#                 aggregation_df.to_excel(writer, sheet_name="aggregation", index=False)
#             bio.seek(0)
#             response = HttpResponse(bio.read())
#             response['content_type'] = 'application/octet-stream'
#             response['Content-Disposition'] = 'attachment; filename=export.xlsx'
#             return response

#         elif action == 'export_json':
#             projects_df = pd.DataFrame(list(projects_qs))
#             date_columns = projects_df.select_dtypes(include=['datetime64[ns, UTC]']).columns
#             for date_column in date_columns:
#                 projects_df[date_column] = projects_df[date_column].dt.tz_localize(None)
#             export_json={"projects":projects_df.to_json(orient='records'),
#                          "rawdata": list(rawdata_qs),
#                          "handle": list(handle_qs),
#                          "preprocessed": list(preprocessed_qs),
#                          "baseline": list(baseline_qs),
#                          "prior_mcmc": list(prior_mcmc_qs),
#                          "bayes_mcmc": list(bayes_mcmc_qs),
#                          "postprocess": list(postprocess_qs),
#                          "aggregation": list(aggregation_qs)}
#             json_str=json.dumps(export_json)
#             response = HttpResponse(json_str, content_type='application/json')
#             response['Content-Disposition'] = 'attachment; filename=export.json'
#             return response

# def read_format(content,nm):
#     if content.name.split('.')[-1] == 'xlsx':
#         df = pd.read_excel(content,sheet_name=nm)
#     elif content.name.split('.')[-1] == 'csv':
#         df = pd.read_csv(content,sheet_name=nm, float_precision='round_trip')
#     return (df)

# def importproj(request,group_name,project_name):
#     with transaction.atomic():
#         request.params = request.GET
#         action = request.params['action']
#         f = request.FILES['content']

#         try:
#             projs.objects.select_for_update().get(project_name=project_name)
#             return JsonResponse({"status": 0, "message": "Project_name has been used. Please rename"})
#         except projs.DoesNotExist:
#             pass
#         try:
#             grp = group.objects.select_for_update().get(group_name=group_name)
#         except group.DoesNotExist:
#             group.objects.select_for_update().create(group_name=group_name)
#             grp = group.objects.select_for_update().get(group_name=group_name)

#         if action == 'import_excel':
#             pj_import = read_format(f, "projects")
#             # pj_import = pd.read_excel(f, sheet_name="projects")
#             projs.objects.select_for_update().create(
#                 project_name=project_name,
#                 group_id=grp.id,
#                 project_status=pj_import['project_status'][0],
#                 mcmc_current_task_id=pj_import['mcmc_current_task_id'][0],
#                 simulation_current_task_id=pj_import['simulation_current_task_id'][0],
#                 # created_datetime=datetime.now(),
#                 # updated_datetime = datetime.now()
#             )

#             pj1 = projs.objects.select_for_update().get(project_name=project_name)

#             try:
#                 rd = read_format(f, "rawdata")
#                 # rd = pd.read_excel(f, sheet_name="rawdata")
#                 rawdata.objects.create(projects=pj1, df_rawdata=rd['df_rawdata'][0],last=True)
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 hd = read_format(f, "handle")
#                 # hd = pd.read_excel(f, sheet_name="handle")
#                 handle.objects.select_for_update().create(
#                     projects=pj1,
#                     last=True,
#                     df_handle=hd['df_handle'][0],
#                     parameters=hd['parameters'][0]
#                 )
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 prepc = read_format(f, "preprocessed")
#                 # prepc= pd.read_excel(f,sheet_name="preprocessed")
#                 preprocessed.objects.create(
#                     projects=pj1,
#                     last=True,
#                     df_chnl=prepc['df_chnl'][0],
#                     parameters=prepc['parameters'][0],
#                     promotion_count=prepc['promotion_count'][0],
#                     y_var=prepc['y_var'][0],
#                     corr=prepc['corr'][0]
#                 )
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 bl = read_format(f, "baseline")
#                 # bl = pd.read_excel(f, sheet_name="baseline")
#                 baseline.objects.select_for_update().create(
#                     projects=pj1,
#                     last=True,
#                     df_mod=bl['df_mod'][0],
#                     df_param_summary_fe=bl['df_param_summary_fe'][0],
#                     df_param_summary_re=bl['df_param_summary_re'][0],
#                     df_metrics=bl['df_metrics'][0],
#                     df_pred=bl['df_pred'][0],
#                     parameters=bl['parameters'][0],
#                     actual_sales_vs_predicted_sales = bl['actual_sales_vs_predicted_sales'][0],
#                     df_metrics_formatted = bl['df_metrics_formatted'][0],
#                     df_param_summary_fe_formatted = bl['df_param_summary_fe_formatted'][0]
#                 )
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 pm = read_format(f, "prior_mcmc")
#                 # pm = pd.read_excel(f, sheet_name="prior_mcmc")
#                 prior_mcmc.objects.select_for_update().create(
#                     projects=pj1,
#                     last=True,
#                     df_info_for_mcmc=pm['df_info_for_mcmc'][0],
#                     df_prior=pm['df_prior'][0],
#                     parameters=pm['parameters'][0])
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 bm = read_format(f, "bayes_mcmc")
#                 # bm = pd.read_excel(f, sheet_name="bayes_mcmc")
#                 bayes_mcmc.objects.select_for_update().create(
#                     projects=pj1,
#                     last=True,
#                     df_stk=bm['df_stk'][0],
#                     df_calculate=bm['df_calculate'][0],
#                     df_bayes_perf=bm['df_bayes_perf'][0],
#                     df_means=bm['df_means'][0],
#                     parameters=bm['parameters'][0],
#                     actual_vs_predicted = bm['actual_vs_predicted'][0],
#                     df_bayes_perf_formatted = bm['df_bayes_perf_formatted'][0],
#                     df_metrics_formatted = bm['df_metrics_formatted'][0],
#                     converge = bm['converge'][0]
#                 )
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 postpc = read_format(f, "postprocess")
#                 # postpc = pd.read_excel(f, sheet_name="postprocess")
#                 postprocess.objects.select_for_update().create(
#                     projects=pj1,
#                     last=True,
#                     df_contr=postpc['df_contr'][0],
#                     df_bs_res=postpc['df_bs_res'][0],
#                     df_prediction=postpc['df_prediction'][0],
#                     df_mod=postpc['df_mod'][0],
#                     df_rawdata=postpc['df_rawdata'][0],
#                     df_cont_out=postpc['df_cont_out'][0],
#                     df_for_mroi=postpc['df_for_mroi'][0],
#                     df_roi_mroi=postpc['df_roi_mroi'][0],
#                     df_index_ci=postpc['df_index_ci'][0],
#                     df_base_n_promo_contr=postpc['df_base_n_promo_contr'][0],
#                     df_response_curve_dict=postpc['df_response_curve_dict'][0],
#                     df_present_impact_factor=postpc['df_present_impact_factor'][0],
#                     parameters=postpc['parameters'][0],
#                     base_vs_incremental_contribution=postpc['base_vs_incremental_contribution'][0],
#                     channel_relative_impact_factor=postpc['channel_relative_impact_factor'][0],
#                     mroi=postpc['mroi'][0],
#                     roi=postpc['roi'][0],
#                     total_promotion_contribution=postpc['total_promotion_contribution'][0],
#                     df_roi_mroi_formatted=postpc['df_roi_mroi_formatted'][0]
#                 )
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 agg = read_format(f, "aggregation")
#                 # agg = pd.read_excel(f, sheet_name="aggregation")
#                 aggregation.objects.select_for_update().create(
#                     projects=pj1,
#                     last=True,
#                     df_bs_roi_agg=agg['df_bs_roi_agg'][0],
#                     df_agg_impact_factor=agg['df_agg_impact_factor'][0],
#                     parameters=agg['parameters'][0],
#                     channel_relative_impact_factor=agg['channel_relative_impact_factor'][0]
#                 )
#             except:
#                 return JsonResponse({"status": 1})

#             return JsonResponse({"status": 1})

#         elif action=='import_json':
#             data = list(f)[0].decode("utf-8")
#             imported_data_tmp=json.dumps(data)
#             imported_data = json.loads(json.loads(imported_data_tmp))

#             projs.objects.select_for_update().create(
#                 project_name=project_name,
#                 group_id=grp.id,
#                 project_status=json.loads(imported_data["projects"])[0]["project_status"],
#                 mcmc_current_task_id=json.loads(imported_data["projects"])[0]["mcmc_current_task_id"],
#                 simulation_current_task_id=json.loads(imported_data["projects"])[0]["simulation_current_task_id"],
#                 # created_datetime=datetime.now(),
#                 # updated_datetime=datetime.now()
#             )

#             pj_import = projs.objects.select_for_update().get(project_name=project_name)

#             try:
#                 rawdata.objects.select_for_update().create(projects=pj_import, df_rawdata=imported_data['rawdata'][0]['df_rawdata'],last=True)
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 handle.objects.select_for_update().create(
#                     projects=pj_import, df_handle=imported_data['handle'][0]['df_handle'], parameters=imported_data['handle'][0]['parameters'],last=True)
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 preprocessed.objects.select_for_update().create(
#                     projects=pj_import,
#                     last=True,
#                     df_chnl=imported_data['preprocessed'][0]['df_chnl'],
#                     parameters=imported_data['preprocessed'][0]['parameters'],
#                     promotion_count = imported_data['preprocessed'][0]['promotion_count'],
#                     y_var = imported_data['preprocessed'][0]['y_var'],
#                     corr = imported_data['preprocessed'][0]['corr'],
#                 )
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 baseline.objects.select_for_update().create(
#                     projects=pj_import,
#                     last=True,
#                     df_mod=imported_data['baseline'][0]['df_mod'],
#                     df_param_summary_fe=imported_data['baseline'][0]['df_param_summary_fe'],
#                     df_param_summary_re=imported_data['baseline'][0]['df_param_summary_re'],
#                     df_metrics=imported_data['baseline'][0]['df_metrics'],
#                     df_pred=imported_data['baseline'][0]['df_pred'],
#                     parameters=imported_data['baseline'][0]['parameters'],
#                     actual_sales_vs_predicted_sales = imported_data['baseline'][0]['actual_sales_vs_predicted_sales'],
#                     df_metrics_formatted = imported_data['baseline'][0]['df_metrics_formatted'],
#                     df_param_summary_fe_formatted = imported_data['baseline'][0]['df_param_summary_fe_formatted']
#                 )

#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 prior_mcmc.objects.select_for_update().create(
#                     projects=pj_import,
#                     last=True,
#                     df_info_for_mcmc=imported_data['prior_mcmc'][0]['df_info_for_mcmc'],
#                     df_prior=imported_data['prior_mcmc'][0]['df_prior'],
#                     parameters=imported_data['prior_mcmc'][0]['parameters'])
#             except:
#                 return JsonResponse({"status": 1})

#             try:
#                 bayes_mcmc.objects.select_for_update().create(
#                     projects=pj_import,
#                     last=True,
#                     df_stk=imported_data['bayes_mcmc'][0]['df_stk'],
#                     df_calculate=imported_data['bayes_mcmc'][0]['df_calculate'],
#                     df_bayes_perf=imported_data['bayes_mcmc'][0]['df_bayes_perf'],
#                     df_means=imported_data['bayes_mcmc'][0]['df_means'],
#                     parameters=imported_data['bayes_mcmc'][0]['parameters'],
#                     actual_vs_predicted = imported_data['bayes_mcmc'][0]['actual_vs_predicted'],
#                     df_bayes_perf_formatted = imported_data['bayes_mcmc'][0]['df_bayes_perf_formatted'],
#                     df_metrics_formatted = imported_data['bayes_mcmc'][0]['df_metrics_formatted'],
#                     converge = imported_data['bayes_mcmc'][0]['converge']
#             )
#             except:
#                 return JsonResponse({"status":1})

#             try:
#                 postprocess.objects.select_for_update().create(
#                     projects=pj_import,
#                     last=True,
#                     df_contr=imported_data['postprocess'][0]['df_contr'],
#                     df_bs_res=imported_data['postprocess'][0]['df_bs_res'],
#                     df_prediction=imported_data['postprocess'][0]['df_prediction'],
#                     df_mod=imported_data['postprocess'][0]['df_mod'],
#                     df_rawdata=imported_data['postprocess'][0]['df_rawdata'],
#                     df_cont_out=imported_data['postprocess'][0]['df_cont_out'],
#                     df_for_mroi=imported_data['postprocess'][0]['df_for_mroi'],
#                     df_roi_mroi=imported_data['postprocess'][0]['df_roi_mroi'],
#                     df_index_ci=imported_data['postprocess'][0]['df_index_ci'],
#                     df_base_n_promo_contr=imported_data['postprocess'][0]['df_base_n_promo_contr'],
#                     df_response_curve_dict=imported_data['postprocess'][0]['df_response_curve_dict'],
#                     df_present_impact_factor=imported_data['postprocess'][0]['df_present_impact_factor'],
#                     parameters=imported_data['postprocess'][0]['parameters'],
#                     base_vs_incremental_contribution = imported_data['postprocess'][0]['base_vs_incremental_contribution'],
#                     channel_relative_impact_factor = imported_data['postprocess'][0]['channel_relative_impact_factor'],
#                     mroi = imported_data['postprocess'][0]['mroi'],
#                     roi = imported_data['postprocess'][0]['roi'],
#                     total_promotion_contribution = imported_data['postprocess'][0]['total_promotion_contribution'],
#                     df_roi_mroi_formatted = imported_data['postprocess'][0]['df_roi_mroi_formatted'],
#                 )
#             except:
#                 return JsonResponse({"status":1})

#             try:
#                 aggregation.objects.select_for_update().create(
#                     projects=pj_import,
#                     last=True,
#                     df_bs_roi_agg=imported_data['aggregation'][0]['df_bs_roi_agg'],
#                     df_agg_impact_factor=imported_data['aggregation'][0]['df_agg_impact_factor'],
#                     parameters=imported_data['aggregation'][0]['parameters'],
#                     channel_relative_impact_factor=imported_data['aggregation'][0]['channel_relative_impact_factor']
#                 )
#             except:
#                 return JsonResponse({"status":1})

#             return JsonResponse({"status":1})


# def forkproj(request, group_name, project_name):
#     with transaction.atomic():
#         params = json.loads(request.body)
#         proj_nm_new = params['project_name_new']
#         try:
#             projs.objects.select_for_update().get(project_name=proj_nm_new)
#             return JsonResponse({"status": 0,"message":"Project_name has been used. Please rename"})
#         except projs.DoesNotExist:
#             pass
#         proj_nm_fork = proj_nm_new
#         # suffix_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
#         # proj_nm_fork = project_name + '_' + 'F'+ suffix_time

#         # grp_nm_new = request.POST.get('group_name', False)
#         # if 'group_name'in request.POST:
#         #     grp_nm_fork=grp_nm_new
#         #     try:
#         #         grp1 = group.objects.select_for_update().get(group_name=grp_nm_fork)
#         #     except group.DoesNotExist:
#         #         group.objects.select_for_update().create(group_name=grp_nm_fork)
#         #         grp1 = group.objects.select_for_update().get(group_name=grp_nm_fork)
#         # else:
#         grp1 = group.objects.select_for_update().get(group_name=group_name)



#         pj1 = projs.objects.select_for_update().get(project_name=project_name,group__group_name=group_name)

#         if pj1.project_status=="BAYES_MCMC_RUNNING":
#             projs.objects.select_for_update().create(
#                 project_name=proj_nm_fork,
#                 group_id=grp1.id,
#                 project_status="PRIOR_MCMC",
#                 mcmc_current_task_id=pj1.mcmc_current_task_id,
#                 simulation_current_task_id=pj1.simulation_current_task_id,
#                 # created_datetime=datetime.now(),
#                 # updated_datetime=datetime.now()
#             )
#         else:
#             projs.objects.select_for_update().create(
#                                               project_name=proj_nm_fork,
#                                               group_id=grp1.id,
#                                               project_status=pj1.project_status,
#                                               mcmc_current_task_id=pj1.mcmc_current_task_id,
#                                               simulation_current_task_id=pj1.simulation_current_task_id,
#                                               # created_datetime=datetime.now(),
#                                               # updated_datetime=datetime.now()
#                                               )
#         pj_fork = projs.objects.select_for_update().get(project_name=proj_nm_fork)

#         try:
#             rd = rawdata.objects.select_for_update().get(projects=pj1,last=True)
#             rawdata.objects.select_for_update().create(projects=pj_fork, df_rawdata=rd.df_rawdata,last=True)
#         except rawdata.DoesNotExist:
#             return JsonResponse({"status":1})

#         try:
#             hd = handle.objects.select_for_update().get(projects=pj1,last=True)
#             handle.objects.select_for_update().create(projects=pj_fork, df_handle=hd.df_handle, parameters=hd.parameters,last=True)
#         except handle.DoesNotExist:
#             return JsonResponse({"status":1})

#         try:
#             preppc = preprocessed.objects.select_for_update().get(projects=pj1,last=True)
#             preprocessed.objects.select_for_update().create(
#                     projects=pj_fork,
#                     last=True,
#                     df_chnl=preppc.df_chnl,
#                     parameters=preppc.parameters,
#                     promotion_count = preppc.promotion_count,
#                     y_var = preppc.y_var,
#                     corr = preppc.corr
#             )
#         except preprocessed.DoesNotExist:
#             return JsonResponse({"status":1})

#         try:
#             bl = baseline.objects.select_for_update().get(projects=pj1,last=True)
#             baseline.objects.select_for_update().create(
#             projects=pj_fork,
#             last=True,
#             df_mod=bl.df_mod,
#             df_param_summary_fe=bl.df_param_summary_fe,
#             df_param_summary_re=bl.df_param_summary_re,
#             df_metrics=bl.df_metrics,
#             df_pred=bl.df_pred,
#             parameters=bl.parameters,
#             actual_sales_vs_predicted_sales=bl.actual_sales_vs_predicted_sales,
#             df_metrics_formatted=bl.df_metrics_formatted,
#             df_param_summary_fe_formatted=bl.df_param_summary_fe_formatted
#         )
#         except baseline.DoesNotExist:
#             return JsonResponse({"status":1})

#         try:
#             pm = prior_mcmc.objects.select_for_update().get(projects=pj1,last=True)
#             prior_mcmc.objects.select_for_update().create(
#             projects=pj_fork,
#             last=True,
#             df_info_for_mcmc=pm.df_info_for_mcmc,
#             df_prior=pm.df_prior,
#             parameters=pm.parameters
#             )
#         except prior_mcmc.DoesNotExist:
#             return JsonResponse({"status": 1})

#         if pj1.project_status=="BAYES_MCMC_RUNNING":
#             return JsonResponse({"status": 1,"message":"original project is in BAYES_MCMC_RUNNING status and new project have been forked to prior_mcmc project_status"})
#         try:
#             bm = bayes_mcmc.objects.select_for_update().get(projects=pj1,last=True)
#             bayes_mcmc.objects.select_for_update().create(
#                 projects=pj_fork,
#                 last=True,
#                 df_stk=bm.df_stk,
#                 df_calculate=bm.df_calculate,
#                 df_bayes_perf=bm.df_bayes_perf,
#                 df_means=bm.df_means,
#                 parameters=bm.parameters,
#                 actual_vs_predicted = bm.actual_vs_predicted,
#                 df_bayes_perf_formatted = bm.df_bayes_perf_formatted,
#                 df_metrics_formatted = bm.df_metrics_formatted,
#                 converge = bm.converge
#             )
#         except bayes_mcmc.DoesNotExist:
#             return JsonResponse({"status": 1})

#         try:
#             postpc = postprocess.objects.select_for_update().get(projects=pj1,last=True)
#             postprocess.objects.select_for_update().create(
#                 projects=pj_fork,
#                 last=True,
#                 df_contr=postpc.df_contr,
#                 df_bs_res=postpc.df_bs_res,
#                 df_prediction=postpc.df_prediction,
#                 df_mod=postpc.df_mod,
#                 df_rawdata=postpc.df_rawdata,
#                 df_cont_out=postpc.df_cont_out,
#                 df_for_mroi=postpc.df_for_mroi,
#                 df_roi_mroi=postpc.df_roi_mroi,
#                 df_index_ci=postpc.df_index_ci,
#                 df_base_n_promo_contr=postpc.df_base_n_promo_contr,
#                 df_response_curve_dict=postpc.df_response_curve_dict,
#                 df_present_impact_factor=postpc.df_present_impact_factor,
#                 parameters=postpc.parameters,
#                 base_vs_incremental_contribution=postpc.base_vs_incremental_contribution,
#                 channel_relative_impact_factor=postpc.channel_relative_impact_factor,
#                 mroi=postpc.mroi,
#                 roi=postpc.roi,
#                 total_promotion_contribution=postpc.total_promotion_contribution,
#                 df_roi_mroi_formatted=postpc.df_roi_mroi_formatted
#             )
#         except postprocess.DoesNotExist:
#             return JsonResponse({"status":1})

#         try:
#             agg = aggregation.objects.select_for_update().get(projects=pj1,last=True)
#             aggregation.objects.select_for_update().create(
#                 projects=pj_fork,
#                 last=True,
#                 df_bs_roi_agg =agg.df_bs_roi_agg ,
#                 df_agg_impact_factor =agg.df_agg_impact_factor ,
#                 parameters=agg.parameters,
#                 channel_relative_impact_factor=agg.channel_relative_impact_factor
#             )
#         except aggregation.DoesNotExist:
#             return JsonResponse({"status":1})

#     return JsonResponse({"status": 1})

