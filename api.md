# Index
* GET /index
+ doc
--------------------------------------

# Project sub page
* GET ``/${group_name}/${project_name}``
+ doc

--------------------------------------
# GROUP API

## Get group list
* GET /api/groups
+ Request (application/json)
+ Response:(application/json)
```
# 权限：Owner 可访问所有,返回全量
# 权限：（auth user） Maintainer每个id不一样界面 
# 项目创建者project privileges在对应项目有所有权限，其他maintainer只有enter，copy，share（只能view  get接口）
{
    "group_meta":{
        {
            "group_privileges":["Create New Group"] # this field is used to decide whether to render 'New Group' bottom on the group page
        }
    },
    "group_list": [
        {
            "group_name": "Benlysta",
            "created_datetime": "2023-02-07T06:58:04.450Z",
            "project_count": 0,
            "group_internal_privileges":["Create New Analysis","Upload"],
            "projects_list": []
        },
        {
            "group_name": "aaa",
            "created_datetime": "2023-02-07T09:23:00.338Z",
            "project_count": 1,
            "group_internal_privileges":["Create New Analysis","Upload"],
            "projects_list": [
                {
                    "project_name": "aaa_1",
                    "project_status": "MODELING",
                    "updated_datetime": "2023-02-07T09:23:00.386Z"
                    "project_privileges:["Publish","Enter","Copy","Share","Delete"]
                }
            ]

        }
    ]
}

# 后端参考
# 权限：Guest 访问时group_privileges blank,project_privileges只有enter，
# share（share表 id相关project list）和publish （projects表 publish_flag=1）的并集  （接口返回的这个list是每个id不一样）

{
    "group_meta":{
        {
            "group_privileges":[] # this field is used to decide whether to render 'New Group' bottom on the group page
        }
    },
    "group_list": [
        {
            "group_name": "Sulperazon",
            "created_datetime": "2023-02-07T06:58:04.450Z",
            "project_count": 0,
            "group_internal_privileges":[],
            "projects_list": []
        },
        {
            "group_name": "aaa",
            "created_datetime": "2023-02-07T09:23:00.338Z",
            "project_count": 1, # 该id当下可见的组下项目数目
            "group_internal_privileges":[],
            "projects_list": [
                {
                    "project_name": "aaa_1",
                    "project_status": "MODELING",
                    "updated_datetime": "2023-02-07T09:23:00.386Z"
                    "project_privileges:["Enter"]
                }
            ]

        }
    ]
}

```
## Create empty group
* PUT /api/groups/${group_name}
+ Request (application/json)
+ Response:(application/json)
```
# 权限：Maintainer+Owner

success:

{
    "status":1
}
```
```
fail:
{
    "status": 0,
    "message": "Group_name has been used. Please rename"
}

```
+ Exception(application/json ? http stats code)
tbd
--------------------------------------
## Delete exsting group
* DELETE /api/groups/${group_name}
+ Request (application/json)
+ Response:(application/json)

```
# 权限：Maintainer creator+ Owner 

{
    "status":int   # 1 success, 0 fail
}
```
+ Exception(application/json ? http status code)
 tbd （不是Maintainer creator+ Owner role的抛错 Unauthorized or Forbidden ）


--------------------------------------
## Rename exsting group
* POST /api/groups/${group_name}/rename
+ Request (application/json)
```
# 权限：Maintainer creator+ Owner 

{
   "group_name_new": str
}
```
+ Response:(application/json)
```
{
    "status":int   # 1 success, 0 fail
}
```
+ Exception(application/json ? http status code)
```
{
    'status': 0,
    'message':'old group_name do not exist'
}
```

--------------------------------------
# PROJECT API

## Get project list
* GET /api/${group_name}/projects
+ Request (application/json)
+ Response:(application/json)
```
# 权限：Owner 可访问所有
# 权限：（auth user） Maintainer每个id不一样界面 
# 项目创建者project privileges有所有权限 其他maintainer只有enter view get接口和copy privileges share是否给？
# Guest 访问时project_privileges只有enter，接口response share（share表 id相关project list）和publish （projects表 publish_flag=1）的并集  的project 
# simulation list里面value为1的是可公开的simulation
{
    "group_name": "Benlysta",
    "projects_list": [
        {
            "project_name": "Benlysta",
            "project_status": "MODEL", # 项目的状态有以下枚举值tbd ["EMPTY","MODEL_RUNNING","MODEL","OUTPUT","SIMULATION_RUNNING""SIMULATION"]
            "updated_datetime": "2023-02-07T07:35:10.862Z",
            "project_privileges:["Publish","Enter","Copy","Share","Delete"],
            "simulations_list": {"simulation1":{"task_id": " ","is_visible":0,"task_status":" "},"simulation2":{"task_id":2222,"is_visible":1,"task_status":"SIMULATION_RUNNING"}}} 
        {
            "project_name": "Benlysta2",
            "project_status": "SIMULATION",
            "updated_datetime": "2023-01-09T00:00:00Z",
            "project_privileges:["Enter","Copy"],
            "simulations_list": {"simulation1":{"task_id": " ","is_visible":0,"task_status":" "},"simulation2":{"task_id":2222,"is_visible":1,"task_status":"SIMULATION_RUNNING"}}
        }
    ]
}

```


## Create empty project
* PUT ``/api/projects/${group_name}/${project_name}``
+ Request (application/json)

```
# 权限：Maintainer+Owner
{
    "brand_name":"nucala",
    "time_period_id": int # only month_id,
    "data_version_id":int #  date like 20250501
}

```

+ Response:(application/json)
```
#success
{
    "status":1 success
}
```
```
#fail
{
    "status": 0,
    "message": "Project_name has been used. Please rename"
}
```
+ Exception(application/json ? http stats code)
```
{
    "status": 0,
    "message":"group_name is not correct"
}
```

--------------------------------------

## Publish project
* POST ``/api/contents/${group_name}/${project_name}/publish``
+ Request:(application/json)
+ Response:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "status":1, # other wise 0
}
```
## cancel Publish project
* POST ``/api/contents/${group_name}/${project_name}/cancel_publish``
+ Request:(application/json)
+ Response:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "status":1, # other wise 0
}
```

## Rename exsting project
* POST ``/api/groups/${group_name}/${project_name}/rename``
+ Request (application/json)
```
# 权限：Maintainer creator+Owner

{
   "project_name_new": str
}
```
+ Response:(application/json)
```
{
    "status":int   # 1 success, 0 fail
}
```
+ Exception(application/json ? http status code)
```
{
    "status": 0,
    "message":"old project_name is not correct"
}
or
{
    "status": 0,
    "message":"group_name is not correct"
}
```

--------------------------------------
## Delete exsting project
* DELETE ``/api/projects/${group_name}/${project_name}``
+ Request (application/json)
+ Response:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "status":int   # 1 success, 0 faile
}
```
+ Exception(application/json ? http status code)
{
    "status":0,
    "Message":"project_name is not correct"
}


--------------------------------------
## Export excel project
* GET ``/api/projects/${group_name}/${project_name}?action=export_excel``
+ Request (application/json)
+ Response:(application/text/plain;charset=UTF-8)
```
# 权限：Maintainer+Owner
{
    "content": binary # file-octstream
}
```
+ Exception(application/json ? http status code)
TBD

## Export json project
* GET ``/api/projects/${group_name}/${project_name}?action=export_json``
+ Request (application/json)
+ Response:(application/json;charset=UTF-8)
```
# 权限：Maintainer+Owner
{
    "content": binary # file-octstream
}
```
+ Exception(application/json ? http status code)
TBD

--------------------------------------

## Import excel project
* POST ``/api/projects/${group_name}/${project_name}?action=import_excel``
+ Request:(application/text/plain;charset=UTF-8)
```
# 权限：Maintainer+Owner
{
    "content": binary, # file-octstream
    "project_name": str # filename read from os
}
```

+ Response:(application/json)
```
#success
{
    "status":1
}

```
```
#fail
{
    "status": 0,
    "message": "Project_name has been used. Please rename"
}
```
+ Exception(application/json ? http status code)
TBD

## Import json project
* POST ``/api/projects/${group_name}/${project_name}?action=import_json``
+ Request:(application/text/plain;charset=UTF-8)
```
# 权限：Maintainer+Owner

{
    "content": binary, # file-octstream
    "project_name": str # filename read from os
}
```

+ Response:(application/json)
```
#success
{
    "status":1
}

```
```
#fail
{
    "status": 0,
    "message": "Project_name has been used. Please rename"
}
```
+ Exception(application/json ? http status code)
TBD

--------------------------------------

## Fork project
* POST ``/api/projects/${group_name}/${project_name}/fork``
+ Request:(application/json)
```
# 权限：Maintainer+Owner
# 跨组fork 一个group只有creator自己的项目 ，非创建者fork 需fork到自己的group

{
    "group_name": str # groupname read from get api tbd (后端思路 id下对应的 /api/groups 下distinct的group_name),
    "project_name_new": str
}
```

+ Response:(application/json)
```
#success
{
    "status":1
}

```
```
#fail
{
    "status": 0,
    "message": "Project_name has been used. Please rename"
}
```
+ Exception(application/json ? http status code)
TBD



## Share project
* POST ``/api/projects/${group_name}/${project_name}/share``
+ Request:(application/json)
```
# 权限：Maintainer+Owner
{
    "mudid": str,
    "type": str # mudid or email address
    "msg":str
    
}
```

+ Response:(application/json)
```
#success
{
    "status":1
}

```
```
#fail
{
    "status": 0,
    "message": "mudid or email address does not exsits" # or other
}
```
+ Exception(application/json ? http status code)
TBD

--------------------------------------
# Contents API

## Preview meta data for empty project
* GET ``/api/contents/${group_name}/${project_name}/meta_data``
+ Request:(application/json)
+ Response:(application/json)
```
# 权限：Maintainer+Owner+有权限的guest
{
    "default_channel_list":[
        "channel_name":str, 
        "channel_prior":int  
    ], # for each project, there is a default_channel_list needed to be rendered for modeling pages
    "default_segmentation_type_list": ["Type:Core,Engine,Others","Type:Lupus_Center,Others"......], # as above
    "brand_name":"Benlysta",
    "time_period_id": int # only month_id
    "data_version_id":int # date like 20250501
    "AB_proportion_list":[
        "AB_proportion_option":str, 
        "AB_proportion":float  
    ], # for each project, there is a AB_proportion_list needed to be rendered for simulation pages
}

```
--------------------------------------

## Run modeling 
* POST ``/api/contents/${group_name}/${project_name}/modeling``
+ Request:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "channel_layout":str # from ["7","9","customized"],

    "channel_agg_rule":{ str:[str,str],str:[str]}, #  "new_column_name1":["old_column_name1","old_column_name2"] --> new_column_name is user input, "old_column_name" is element from /api/contents/${group_name}/${project_name}/empty/meta_data key default_channel_list key channel_name

    "prior":[
        "channel_name":str,
        "channel_prior":int
    ], # all element from /api/contents/${group_name}/${project_name}/empty/meta_data key default_channel_list
    "segmentation_type": str $ get element from /api/contents/${group_name}/${project_name}/empty/meta_data key default_segmentation_type_list
    
}
```
+ Response:(application/json)
```
{
    "status":int, # 1 success, 0 fail
    "task_id":str  # this should be run id returned from Databricks api
}
```
+ Exception(application/json ? http status code)
TBD                                                                                                                                                                                        

## Get current model asnyc task
* GET ``/api/contents/${group_name}/${project_name}/modeling/current_task``
+ Request:(application/json)
+ Response:(application/json)
```
# 权限：Maintainer+Owner+有权限的guest
{
    "task_status":str # one of the value {FAILURE|PENDING|RECEIVED|RETRY|REVOKED|STARTED|SUCCESS},
    "task_id":str  # get from databricks async api
}
```
## Revoke current model asnyc task
* DELETE ``/api/contents/${group_name}/${project_name}/modeling/current_task``
+ Request:(application/json)
+ Response:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "status":int # 1 success, 0 fail
}
```
+ Exception(application/json)
TBD

## Preview modeling output
* GET ``/api/contents/${group_name}/${project_name}/modeling/metadata|parameters|result?segmentation_type=Total Market``
+ Request:(application/json)
+ Response:(application/json)
```
#权限：Maintainer+Owner+有权限的guest
#case
#when metadata
{
    "Output_time":"2025-07-03",
    "Model_time_period":"202307-202506",
    "aggregate_channel_list":["F2F call",'HT',...]
}

#when parameters
#this parameters is rendered when the project stats is set to MODELING, on modeling paramters page.
#when the project state is EMPTY, the modeling parameters page should be set by api ``/api/contents/${group_name}/${project_name}/meta_data``
{


    "channel_layout":int # from ["7","9","customized"],
    "channel_agg_rule":{ str:[str,str],str:[str]}, #  "new_column_name1":["old_column_name1","old_column_name2"] --> new_column_name is user input, "old_column_name" is element from /api/contents/${group_name}/${project_name}/empty/meta_data key default_channel_list key channel_name
    "prior":[
        "channel_name":str,
        "channel_prior":int
    ], # all element from /api/contents/${group_name}/${project_name}/empty/meta_data key default_channel_list
    "segmentation_type": str $ get element from /api/contents/${group_name}/${project_name}/empty/meta_data key default_segmentation_type_list

}
#when result with segmentation_type parameter
{
    "Total_Cost":"1,453M",
    "Total_Sales":"1,960M",
    "Total_Cost_Total_Sales": "74.13%",
    "Cost_Distribution": object , # this structure is depending on front end object layout of circle graph
    "Current_Unit_Price": Datframe to dict layout?
    "Cost_by_Channels_VS_Total_sales_trend": object, # this structure is depending on front end object layout of line graph     
    "Touch_Points_by_Channel_VS_Total_Sales_Trend" : object, # this structure is depending on front end object layout of line graph
    "Promotion_vs_Non_promotion": object, this structure is depending on front end object layout of bar graph
    "Total_promotion_contribution": object,  this structure is depending on front end object layout of circle graph
    "ROI_MROI":object,
    "Response_curve":object,
    "Model_Metrics": pandas.to_dict?
}
```
+ Exception(application/json ? http status code)
TBD

--------------------------------------

## Add simulation
* PUT ``/api/contents/${group_name}/${project_name}/${simulation_name}``
+ Request:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "Optimization_Type": str, #"MCCP suggestion"|"Fixed Budget"
    "MCCP_cycle":int # 202502 month_id like integer representing year/month
} 
```
+ Response:(application/json)
```
{
    "status":1, # successfully
}
```


## Preview Simulation metadata
* GET ``/api/contents/${group_name}/${project_name}/${simulation_name}/meta_data``
+ Response:(application/json)
```
#权限：Maintainer+Owner 看到是所有的simulation  check权限
#权限：有权限的guest  看到是visible的simulation  check权限
{
    "Optimization_Type" : str, # "MCCP suggestion"|"Fixed Budget"
    "Time_Period": 6, #months
    "Budget": 0,
    "Unit_Price_and_Constraints': [
        {
            "Channel":"F2F call",
            "Unit_Price": float,
            "If_changes":"unchanged",
            "Change_percentage":0,
            "Channel_Contraint":bool,
            "Min_Spend": float,
            "Max_Spend": float,
            # AB_proportion only for Optimization Type=Fixed Budget and default AB_proportion_option=no weight , default AB_proportion is 1
            "AB_proportion_option": "no weight"|"past 12 months"|"past 6 months"|"past 3 months",  # get element from /api/contents/${group_name}/${project_name}/empty/meta_data key AB_porportion_list key AB_proportion_option ,
            "AB_proportion":float,  # get element from /api/contents/${group_name}/${project_name}/empty/meta_data key AB_porportion_list key AB_proportion  (only for  F2F_CALL and HT channel)
            "field_configurable":["Unit Price","Min Spend","Max Spend","AB_proportion"]
        }
    ]

}
```

## Run simulation
* POST ``/api/contents/${group_name}/${project_name}/${simulation_name}/run``
+ Request:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "Optimization_Type" : "Fixed Budget"|"MCCP suggestion", 
    "Time_Period": int, #months
    "Budget": int,
    "Unit_Price_and_Constraints': [

        {
            "Channel":"F2F call","
            "Unit_Price":"float", 
            "If_changes":"unchanged",
            "Change_percentage":float, 
            "Channel_Contraint":bool, 
            "Min_Spend": float,
            "Max_Spend": float,
            # only for Optimization Type=Fixed Budget and default AB_proportion_option=no weight , AB_proportion is 1
            "AB_proportion_option": "no weight"|"past 12 months"|"past 6 months"|"past 3 months",  # get element from /api/contents/${group_name}/${project_name}/empty/meta_data key AB_porportion_list key AB_proportion_option  ,
            "AB_proportion":float,  # get element from /api/contents/${group_name}/${project_name}/empty/meta_data key AB_porportion_list key AB_proportion  (only for  F2F_CALL and HT channel)
        }
    ]
}
``` 
+ Response:(application/json)
```
{
    "status":int, # 1 success, 0 fail
    "task_id":str  # this should be run id returned from Databricks api
}

```
## Check current async task and Delete current task is the same as modeling one

## Get current model asnyc task
* GET ``/api/contents/${group_name}/${project_name}/${simulation_name}/modeling/current_task``
+ Request:(application/json)
+ Response:(application/json)
```
# 权限：Maintainer+Owner+有权限的guest
{
    "task_status":str # one of the value {FAILURE|PENDING|RECEIVED|RETRY|REVOKED|STARTED|SUCCESS},
    "task_id":str  # get from databricks async api
}
```
## Revoke current model asnyc task
* DELETE ``/api/contents/${group_name}/${project_name}/${simulation_name}/modeling/current_task``
+ Request:(application/json)
+ Response:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "status":int # 1 success, 0 fail
}
```
+ Exception(application/json)
TBD

## Preview simulations
* GET ``/api/contents/${group_name}/${project_name}/${simulation_name}/list``
+ Response:(application/json)
```
#权限：Maintainer+Owner+有权限的guest
         {   
              "simulation_parameters":{}, # this format is exactly the same as the run api ``/api/contents/${group_name}/${project_name}/${simulation_name}/run``
              "Optimal_Channel_Performance": pandas.to_dict() structure,
              "Current_Chaneel_Performance": pandas.to_dict() structure,
              "Simulated_Performance":{
                  "Promotion_VS_Non_promotion": object, layout depending on frontend bar graph
                  "Total_promotion_Contribution": object, layout depending on front end circle graph
                  "ROI_MROI":object this is nested object,  layout depending on front end line graph
                  "Cost_Distribution": object, layout depending on front end circle graph
                  "Caculated_Unit_Price": pandas.to_dict()
              },
              "Current_Performance": # almost same as /api/contents/${group_name}/${project_name}/modeling/result?segmentation_type=Total Market
              {
                  "Promotion_VS_Non_promotion": object, layout depending on frontend bar graph
                  "Total_promotion_contribution": object, layout depending on front end circle graph
                  "ROI_MROI":object this is nested object,  layout depending on front end line graph
                  "Cost_Distribution": object, layout depending on front end circle graph
                  "Current_Unit_Price": pandas.to_dict()
              },
         }

```
## Delete simulation
* DELETE ``/api/contents/${group_name}/${project_name}/${simulation_name}``
+ Request:(application/json)
+ Response:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "status":1, # other wise 0
}
```
## simulation Visibility
* POST ``/api/contents/${group_name}/${project_name}/simulation_visibility``
+ Request:(application/json)
```
# 权限：Maintainer creator+Owner
{
    "simulation1":0,
    "simulation2":1
}
``` 
+ Response:(application/json)
```
{
    "status":1, # other wise 0
}
```
--------------------------------------
# Django ORM model:
+ There should be 7 Models in Django ORM, 4 for data and 2 for status control
+ rawdata,modeling,simulation

```
from django.db import models

class role(models.Model):
    user_id = models.CharField(max_length=255,primary_key=True)
    name=models.CharField()
    role=models.CharField(default='Guest')   # 枚举值 ["Guest","Maintainer","Owner"]
    add_datetime= models.DateTimeField()
    update_datetime= models.DateTimeField(null=True)
    delete_datetime = models.DateTimeField(null=True)
    is_active=models.BooleanField(default=1)
    roleoptions=models.CharField()
    activity=models.CharField()

class share_project(models.Model):
    pk = models.CompositePrimaryKey("user_id", "project_name")
    user_id = models.CharField() #选项导航栏guest的id options
    msg=models.CharField(null=Ture) 
    project_name =models.ForeignKey(Project, on_delete=models.CASCADE)

class group(models.Model):
    group_name = models.CharField(max_length=255, primary_key=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    delete_datetime = models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=0)
    project_count=  models.IntegerField(default=0) 
    group_privileges=models.CharField(max_length=500) # ['create group','create new analysis','upload']  

class projects(models.Model):
    pk = models.CompositePrimaryKey("group", "project_name")
    project_name = models.CharField(max_length=255)
    project_status = models.CharField(max_length=30) # 枚举值 ["EMPTY","MODELING","SIMULATION"]
    mcmc_current_task_id = models.CharField(max_length=100, null=True)
    simulation_current_task_id = models.CharField(max_length=100, null=True)
    simulations_list=models.CharField(max_length=500, null=True) #tbd
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    delete_datetime = models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=0)
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    project_privileges=models.CharField(max_length=500)   
    is_publish= models.BooleanField(default=0) 
    user_id=models.ForeignKey(role, on_delete=models.CASCADE) 
    
class rawdata(models.Model):
    
    df_rawdata = models.TextField()
    df_data_ab_others== models.TextField()
    brand_name= models.TextField()
    time_period_id= models.TextField()
    data_version_id= models.TextField()
    ori_channel_list models.TextField()
    ori_channel_prior= models.TextField()
    ori_segment= models.TextField()
    last = models.BooleanField()
    projects = models.ForeignKey(projects, on_delete=models.CASCADE)

class mmm(models.Model):
    
    parameters= models.TextField()
    agg_chnl_list= models.TextField()
    segmentation_type= models.TextField()
    rawdata_unscaled_dict = models.TextField()
    rawdata_scaled_dict = models.TextField()
    digital_gsk_impute = models.TextField()
    average_pirce_orig = models.TextField()
    average_pirce_agg= models.TextField()
    average_count_orig= models.TextField()
    average_count_agg= models.TextField()
    total_cost_sales_ratio= models.TextField()
    cost_dist= models.TextField()
    line_trend_dist= models.TextField()
    extra_features_1= models.TextField()
    r_square_mape= models.TextField()
    channel_contribution= models.TextField() 
    base_contribution= models.TextField()
    roi_mroi= models.TextField()
    mmm= models.TextField()
    last = models.BooleanField()
    projects = models.ForeignKey(projects, on_delete=models.CASCADE)

class simulation(models.Model):

    pk = models.CompositePrimaryKey("simulation_name", "projects")
    simulation_name= models.CharField() 
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
    is_visible=models.BooleanField(default=0)

```