# PickMeUp

## Deploy Link: https://prod-pvnxn5ufaq-uc.a.run.app/api/REQUEST/

### Routes 

Register a user for first signup. <br/>
`POST` `/api/register/`
```json
Request 

{
    "name": "<STRING: USER INPUT>", 
    "email": "<STRING: USER INPUT>", 
    "password": "<STRING: USER INPUT>"
}
```

```json
Response

{
  "success": true, 
  "data": 
      {
          "id": "<INT: USER ID>",
          "session_token": "<STRING: SESSION TOKEN>", 
          "session_expiration": "<STRING: DATE-TIME>", 
          "update_token": "<STRING: UPDATE TOKEN>"
        }
}
```

Login a user. <br/>
`POST` `/api/login/`
```json
Request 

{ 
    "email": "<STRING: USER INPUT>", 
    "password": "<STRING: USER INPUT>"
}
```

```json
Response

{
  "success": true, 
  "data": 
      {
          "id": "<INT: USER ID>",
          "session_token": "<STRING: SESSION TOKEN>", 
          "session_expiration": "<STRING: DATE-TIME>", 
          "update_token": "<STRING: UPDATE TOKEN>"
        }
}
```

Update user session. <br/>
`POST` `/api/update_session/`
```json
Request 

{ 
    "authorization": "<STRING: UPDATE TOKEN>"
}
```

```json
Response

{
  "success": true, 
  "data": 
      {
          "session_token": "<STRING: SESSION TOKEN>", 
          "session_expiration": "<STRING: DATE-TIME>", 
          "update_token": "<STRING: UPDATE TOKEN>"
        }
}
```

Get all the possible data categories. <br/>
`GET` `/api/categories/`
```json
Response

{
  "success": true, 
  
  "data": [
        {
          "id": 1,
          "category": "pets"
        }, 
        {
          "id": 2, 
          "category": "food"
        },
        "..." 
    ]
}
```

Get photos of specific category. <br/>
`POST` `/api/data/`
```json
Request 

{ 
    "authorization": "<STRING: SESSION TOKEN>",
    "category": "<STRING: USER INPUT>"
}
```

```json
Response

{
  "success": true, 
  "data": 
        {
          "id": "<INT: PHOTO ID>", 
          "category": "<STRING: CATEGORY NAME>",
          "photo": "<STRING: PHOTO URL>",
          "photographer": "<STRING: PHOTOGRAPHER NAME> - Uploaded to Pexel Photos"
        },
        {
          "id": "<INT: PHOTO ID>", 
          "category": "<STRING: CATEGORY NAME>",
          "photo": "<STRING: PHOTO URL>",
          "photographer": "<STRING: PHOTOGRAPHER NAME> - Uploaded to Pexel Photos"
        },
        ...
}
```

Get photos from user's categories. <br/>
`POST` `/api/data/<int:user_id>/`
```json
Request 

{ 
    "authorization": "<STRING: SESSION TOKEN>",
    "category": "<STRING: USER INPUT>"
}
```

```json
Response

{
  "success": true, 
  "data": 
        {
          "id": "<INT: PHOTO ID>", 
          "category": "<STRING: CATEGORY NAME>",
          "photo": "<STRING: PHOTO URL>",
          "photographer": "<STRING: PHOTOGRAPHER NAME> - Uploaded to Pexel Photos"
        },
        {
          "id": "<INT: PHOTO ID>", 
          "category": "<STRING: CATEGORY NAME>",
          "photo": "<STRING: PHOTO URL>",
          "photographer": "<STRING: PHOTOGRAPHER NAME> - Uploaded to Pexel Photos"
        },
        ...
}
```

Add category to user preferences. <br/>
`POST` `/api/<int:user_id>/category`
```json
Request 

{ 
    "authorization": "<STRING: SESSION TOKEN>",
    "category": "<STRING: USER INPUT>"
}
```

```json
Response

{
  "success": true, 
  "data": 
        {
          "id": "<INT: USER ID>",
          "email": "<STRING: USER EMAIL>",
          "categories": [{
              "id": "<INT: CATEGORY ID>",
              "category": "<STRING: CATEGORY NAME>"
            },
            {
              "id": "<INT: CATEGORY ID>",
              "category": "<STRING: CATEGORY NAME>"
            },
            ...
          ]
        }
        ...
}
```

Remove category from user preferences. <br/>
`DELETE` `/api/<int:user_id>/category`
```json
Request 

{ 
    "authorization": "<STRING: SESSION TOKEN>",
    "category": "<STRING: USER INPUT>"
}
```

```json
Response

{
  "success": true, 
  "data": 
        {
          "id": "<INT: USER ID>",
          "email": "<STRING: USER EMAIL>",
          "categories": [{
              "id": "<INT: CATEGORY ID>",
              "category": "<STRING: CATEGORY NAME>"
            },
            {
              "id": "<INT: CATEGORY ID>",
              "category": "<STRING: CATEGORY NAME>"
            },
            ...
          ]
        }
        ...
}
```

Get a quote of specific theme. <br/>
`POST` `/api/quote/`
```json
Request 

{ 
    "authorization": "<STRING: SESSION TOKEN>",
    "category": "<STRING: USER INPUT>"
}
```

```json
Response

{
  "success": true, 
  "data": 
        {
          "category": "<STRING: QUOTE THEME>",
          "quote": "<STRING: QUOTE>",
          "author": "<STRING: AUTHOR>"
        }
        ...
}
```
