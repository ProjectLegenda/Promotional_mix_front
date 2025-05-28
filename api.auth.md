## Permission List

- GET /api/permissions

* Request (application/json)
* Response:(application/json)

```
[
    {
      id: 12324022,
      name: 'name1',
      role: 'Maintainer',
      activity: ['change', 'remove'],
      roleOptions: ['Maintainer', 'Guest'] # when change role
    },
    {
      id: 12324023,
      name: 'name2',
      role: 'Owner',
      activity: ['change', 'remove'],
      roleOptions: ['Maintainer', 'Guest']
    },

]

```

## Add permission user

- PUT /api/permission/add

* Response:(application/json)
* Request:(application/json)

```
{
    "user_name":str,
    "id": str
    "role": str, #"Maintainer"|"Guest"
}
```

- Response:(application/json)

```
{
    "status":1, # successfully
}
```

## Remove permission user

- DELETE /api/permission/${id}

* Request (application/json)
* Response:(application/json)

```
{
    "status":int   # 1 success, 0 fail
}
```

## Update permission user

- POST /api/permission/${id}/update

* Request (application/json)

```
{
   "role_new": str
}
```

- Response:(application/json)

```
{
    "status":int   # 1 success, 0 fail
}
```

- Exception(application/json ? http status code)

```
{
    'status': 0,
    'message':'Failed to complete the update operation.'
}
```
