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
{
    "group_meta":{
        {
            "privileges":["create"] # this field is used to decide whether to render 'New Group' bottom on the group page
        }
    },
    "group_list": [
        {
            "group_name": "Sulperazon",
            "created_datetime": "2023-02-07T06:58:04.450Z",
            "project_count": 0,
            "privileges":["create","upload"],
            "projects_list": []
        },
        {
            "group_name": "aaa",
            "created_datetime": "2023-02-07T09:23:00.338Z",
            "project_count": 1,
            "projects_list": [
                {
                    "project_name": "aaa_1",
                    "project_status": "MODELING",
                    "updated_datetime": "2023-02-07T09:23:00.386Z"
                    "privileges:["Enter","Copy","Share","Delete"]
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
TBD
--------------------------------------
## Delete exsting group
* DELETE /api/groups/${group_name}
+ Request (application/json)
+ Response:(application/json)
```
{
    "status":int   # 1 success, 0 fail
}
```
+ Exception(application/json ? http status code)
TBD
--------------------------------------
## Rename exsting group
* POST /api/groups/${group_name}/rename
+ Request (application/json)
```
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
{
    "group_name": "sulperzon",
    "projects_list": [
        {
            "project_name": "sulperzon_ge",
            "project_status": "MODELING",   # 项目的状态有以下枚举值 ["EMPTY","MODELING","SIMULATION"]
            "updated_datetime": "2023-02-07T07:35:10.862Z",
            "privileges:["Enter","Copy","Share","Delete"],
            "simulations_list": ["simulation1","simulation2"] #
        },
        {
            "project_name": "sulperzon_hbu",
            "project_status": "SIMULATION",
            "updated_datetime": "2023-01-09T00:00:00Z",
            "privileges:["Enter","Copy","Share","Delete"],
            "simulations_list": ["simulation1","simulation2"] #
        }
    ]
}


```


## Create empty project
* PUT ``/api/projects/${group_name}/${project_name}``
+ Request (application/json)
```
{
    "brand_name":"nucala",
    "time_period_id": int # only month_id
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
## Rename exsting project
* POST ``/api/groups/${group_name}/${project_name}/rename``
+ Request (application/json)
```
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
{
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
{
    "modid": str,
    "type": str # modid or email address
    
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
    "message": "modid does not exsits" # or other
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
{
    "default_channel_list":[
        "channel_name":str, 
        "channel_prior":int  
    ], # for each project, there is a default_channel_list needed to be rendered for modeling pages
    "default_segmentation_type_list": [], # as above
    "brand_name":"nucala",
    "time_period_id": int # only month_id
}

```
--------------------------------------

## Run modeling 
* POST ``/api/contents/${group_name}/${project_name}/modeling``
+ Request:(application/json)
```
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
{
    "status":int # 1 success, 0 fail
}
```
+ Exception(application/json)
TBD

## Preview modeling output
* GET ``/api/contents/${group_name}/${project_name}/modeling/metadata|parameters|result?=segmentation_type=Total Market``
+ Request:(application/json)
+ Response:(application/json)
```
#case
#when metadata
{
    "Output time":"2025-07-03",
    "Model time period":"2023011 - 202506",
    "aggregate_channel_list":["F2F call"]
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
    "Total Cost":"1,453M",
    "Total Sales":"1,960M",
    "Total Cost/Total Sales": "74.13%",
    "Cost Distribution": object , # this structure is depending on front end object layout of circle graph
    "Current Unit Price": Datframe to dict layout?
    "Cost by Channels VS Total sales trend": object, # this structure is depending on front end object layout of line graph     
    "Touch Points by Channel VS Total Sales Trend" : object, # this structure is depending on front end object layout of line graph
    "Promotion vs Non-promotion": object, this structure is depending on front end object layout of bar graph
    "Total promotion contribution": object,  this structure is depending on front end object layout of circle graph
    "ROI/MROI":object,
    "Response curve":object,
    "Model Metrics": pandas.to_dict?
}
```
+ Exception(application/json ? http status code)
TBD


--------------------------------------

## Add simulation
* PUT ``/api/contents/${group_name}/${project_name}/simulation/add``
+ Request:(application/json)
```
{
    "simulation_name":str,
    "Optimization Type": str, #"MCCP suggestion"|"Fixed Budget"
    "MCCP cycle":int # 20250225 month_id like integer representing year/month
} 
```
+ Response:(application/json)
```
{
    "status":1, # successfully
    "simulation_id": int
}
```


## Preview Simulation metadata
* GET ``/api/contents/${group_name}/${project_name}/simulation/meta_data``
+ Response:(application/json)
```
{
    "Optimization Type" : str, # "MCCP suggestion"|"Fixed Budget"
    "Time Period": 6, #months
    "Budget": 0,
    "Unit Price and Constraints': [

        {
            "Channel":"F2F call",
            "Unit Price": float,
            "If changes":"unchanged",
            "Change percentage":0,
            "Channel Contraint":bool,
            "Min Spend": float,
            "Max Spend": float,
            "field_configurable":["Unit Price","Min Spend","Max Spend"]
        }
    ]

}
```

## Run simulation
* POST ``/api/contents/${group_name}/${project_name}/simulation/run``
+ Request:(application/json)
```
{
    "simulation_id":int # simulation_id
    "Optimization Type" : "Fixed Budget"|"MCCP suggestion", 
    "Time Period": int, #months
    "Budget": int,
    "Unit Price and Constraints': [

        {
            "Channel":"F2F call","
            "Unit Price":"float", 
            "If changes":"unchanged",
            "Change percentage":float, 
            "Channel Contraint":bool, 
            "Min Spend": float,
            "Max Spend": float
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

## Preview simulations
* GET ``/api/contents/${group_name}/${project_name}/simulation/list``
+ Response:(application/json)
```
{
    "simulation_list":[
         {   
              "simulation_id":int,
              "simulation_name": str,
              "simulation_parameters":{}, # this format is exactly the same as the run api ``/api/contents/${group_name}/${project_name}/simulation/run``
              "Optimal Channel Performance": pandas.to_dict() structure,
              "Current Chaneel Performance": pandas.to_dict() structure,
              "Simulated Performance":{
                  "Promotion VS Non-promotion": object, layout depending on frontend bar graph
                  "Total promotion Contribution": object, layout depending on front end circle graph
                  "ROI/MROI":object this is nested object,  layout depending on front end line graph
                  "Cost Distribution": object, layout depending on front end circle graph
                  "Caculated Unit Price": pandas.to_dict()
              },
              "Current Performance":{
                  "Promotion VS Non-promotion": object, layout depending on frontend bar graph
                  "Total promotion Contribution": object, layout depending on front end circle graph
                  "ROI/MROI":object this is nested object,  layout depending on front end line graph
                  "Cost Distribution": object, layout depending on front end circle graph
                  "Caculated Unit Price": pandas.to_dict()
              },
         }
    ]
}
```
## Publish simulation
* POST ``/api/contents/${group_name}/${project_name}/simulation/publish``
+ Request:(application/json)
```
{
    simulation_id:int,
}

```
+ Response:(application/json)
```
{
    "status":1, # other wise 0
    "Message": str # returned from backend
}
```
## Delete simulation
* DELETE ``/api/contents/${group_name}/${project_name}/simulation``
+ Request:(application/json)
```
{
    "simulation_id":int,
}
```
+ Response:(application/json)
```
{
    "status":1, # other wise0
    "Message":str
}
```


