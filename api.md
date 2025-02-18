# Index
* GET /index
+ doc
--------------------------------------

# Project sub page
* GET /${group\_name}/${project_name}
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
            "privileges":["create"]
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
* PUT /api/projects/${group_name}/${project_name}
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
* POST /api/groups/${group_name}/${project_name}/rename
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
* DELETE /api/projects/${group_name}/${project_name}
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
* GET /api/projects/${group_name}/${project_name}?action=export_excel
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
* GET /api/projects/${group_name}/${project_name}?action=export_json
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
* POST /api/projects/${group_name}/${project_name}?action=import_excel
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
* POST /api/projects/${group_name}/${project_name}?action=import_json
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
* POST /api/projects/${group_name}/${project_name}/fork
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
* POST /api/projects/${group_name}/${project_name}/share
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
# contents API

## Preview default parameter for empty project
* GET /api/contents/${group_name}/${project_name}/default_parameters
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
* POST /api/contents/${group_name}/${project_name}/modeling
+ Request:(application/json)
```
{
    "channel_layout":int # from ["7","9","customized"],

    "channel_agg_rule":{ str:[str,str],str:[str]}, #  "new_column_name1":["old_column_name1","old_column_name2"] --> new_column_name is user input, "old_column_name" is element from /api/contents/${group_name}/${project_name}/empty/default_parameters key default_channel_list key channel_name

    "prior":[
        "channel_name":str,
        "channel_prior":int
    ], # all element from /api/contents/${group_name}/${project_name}/empty/default_parameters key default_channel_list
    "segmentation_type": str $ get element from /api/contents/${group_name}/${project_name}/empty/default_parameters key default_segmentation_type_list
    
}
```
Response:(application/json)
```
{
    "status":int, # 1 success, 0 fail
    "task_id":str  # this should be run id returned from Databricks api
}
```
+ Exception(application/json ? http status code)
TBD                                                                                                                                                                                        


