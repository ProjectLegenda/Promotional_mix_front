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
            "project_status": "MODELING",
            "updated_datetime": "2023-02-07T07:35:10.862Z",
            "privileges:["Enter","Copy","Share","Delete"]
            
        },
        {
            "project_name": "sulperzon_hbu",
            "project_status": "SIMULATION",
            "updated_datetime": "2023-01-09T00:00:00Z",
            "privileges:["Enter","Copy","Share","Delete"]
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



















