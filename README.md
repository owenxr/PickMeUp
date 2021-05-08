# PickMeUp

### Working Routes 

Register a user for first signup.
Responds with session token, session expiration, and update token. <br/>
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
          "id": 5,
          "category": "fashion"
        }, 
        {
          "id": 2, 
          "category": "food"
        } 
        "..." 
    ]
}
```
