# Index
* GET /index
+ doc
--------------------------------------

# Project sub page
* GET /${group_name}/${project_name}
+ doc

--------------------------------------
# GROUP API

## Get group list
* GET /api/groups
+ Request (application/json)
+ Response:(application/json)
```
{
    "group_list": [
        {
            "group_name": "Sulperazon",
            "created_datetime": "2023-02-07T06:58:04.450Z",
            "project_count": 0,
            "privileges":["create","upload"]
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
