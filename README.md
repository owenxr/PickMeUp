# PickMeUp
The Feel Good App - Browse images you'll like and recieve quotes to brighten your day. <br/>
<br/>
*Note that this app was built to be suitable for Google SQL (mySQL server) and Google Cloud Run (Container Deployment)*
<br/>
<br/>
### ANDROID REPO: [GITHUB](https://github.com/nct33/PickMeUp)

### VIDEO SUBMISSION: [Advertisement](https://www.youtube.com/watch?v=celL7_39VyU)

### Deploy Link
Link: No Longer in Service.

# Features
<img width="375" alt="Screen Shot 2021-05-13 at 12 30 12 AM" src="https://user-images.githubusercontent.com/67097401/118077657-87c6b880-b382-11eb-809b-405de1c28636.png">

* Registration and Login

<img width="375" alt="Screen Shot 2021-05-13 at 12 30 22 AM" src="https://user-images.githubusercontent.com/67097401/118077662-8ac1a900-b382-11eb-8683-5c1be75c684a.png">

* Selecting Categories to View

![Splash](https://user-images.githubusercontent.com/67097401/118077710-a036d300-b382-11eb-934f-791e0eba896f.png)

* Scroll Through Photos and Quotes

# Table Of Contents
* [Setup](#Setup)
* [Final Submission Requirements](#Final-submission-requirements)
* [API Specifications](#API-Specifications)
* [Extra Cool Stuff](#Extra-cool-stuff)

# Setup

### Clone Repository
Clone repository `$ git clone https://www.github.com/owenxr/pickmeup.git` <br/>
Navigate to "src," create a venv, and run `pip3 install -r requirements.txt` <br/>

### Create API Keys
Register and Generate API Keys using the following links
* [Quotes API](https://rapidapi.com/yusufnb/api/quotes)
* [Photos/Videos API](https://www.pexels.com/api/) <br/>
*Free usage of API's limits the number of calls we can make. It is also difficult to find API's that are both free and allow automated usage.*

### Editing app.py

Pay attention to lines 17-33 of `app.py`. 
* If you will be using Sqlite3 with SQLAlchemy, (Untested)
    * In the "src" directory, create a `vars.config` file structured below and replace key values
    * ```config
      [APIKEY]
      pexels_key = <PEXELS API KEY>
      quotes_key = <QUOTES API KEY>
      quotes_host = yusufnb-quotes-v1.p.rapidapi.com
      ```
    * Delete lines 42-57 and replace 17-33 with 
    * ```python
    
      configParser = ConfigParser() 
      configParser.read('<RELATIVE PATH TO VARS.CONFIG>/vars.config') 
      #If app.py cannot find section APIKEY, chances are the file was not found

      db_filename = "pickmeup.db"

      app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
      app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
      app.config["SQLALCHEMY_ECHO"] = True
      ```
* Otherwise, replace lines 17-22 and 42-57 with the necessary values to connect to your database,
    * In the "src" directory, create a `vars.config` file structured below and replace/add/remove key values as needed
    * ```config
      [DBVARS]
      user = <Username>
      pass = <Password>
      name = <Database Name>
      host = <Database IP>
      port = <Database Port>

      [APIKEY]
      pexels_key = <PEXELS API KEY>
      quotes_key = <QUOTES API KEY>
      quotes_host = yusufnb-quotes-v1.p.rapidapi.com
      ```
    * Make sure to include 
    * ```python
    
      configParser = ConfigParser() 
      configParser.read('<RELATIVE PATH TO VARS.CONFIG>/vars.config') 
      #If app.py cannot find section APIKEY, chances are the file was not found
      ```
    * To ensure that you will be able to read the needed values in `app.py`

### Running app.py
Navigate to "src" and run `$ python3 app.py`

# Final Submission Requirements
* [At Least 4 Endpoints](#API-Specifications)
* [API Specification](#API-Specifications)
* Relationship Database schema
    * Look at lines 11-14 in `db.py`
    * Used Many-to-Many association between Users and Categories they like
    * Use One-to-Many relation between Categories and Data relating to it
* [Deployment](#Deploy-link)

# API Specifications 

* User Management
    * [Register](#Register)
    * [Get User's Information](#Get-User-Info)
    * [Login](#Login)
    * [Update Session](#Update-session)
    * [Attach Preference to User](#Add-category-to-user-preferences)
    * [Remove Preference from User](#Remove-category-from-user-preferences)
* Content Management
    * [List Categories](#Get-categories)
    * [Retrieve Photos in a Category](#Get-photos-of-category)
    * [Retrieve Photos in User's Categories](#Get-photos-user-will-like)
    * [Get Themed Quote](#Get-themed-quote)
    * [Get Random Quote in User's Categories](#Get-random-quote-for-user)

### Register
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
	  "name": "<STRING: USER NAME>",
	  "email": "<STRING: EMAIL>",
          "session_token": "<STRING: SESSION TOKEN>", 
          "session_expiration": "<STRING: DATE-TIME>", 
          "update_token": "<STRING: UPDATE TOKEN>"

        }
}
```

### Get User Info
`POST` `/api/info/<int:user_id>/`
```json
Request 

{ 
    "authorization": "<STRING: SESSION TOKEN>"
}
```

```json
Response

{
  "success": true, 
  "data": 
	{
       	    "id": "<INT: USER ID>",
	    "name": "<STRING: USER NAME>",
	    "email": "<STRING: EMAIL>",
	    "categories": [
	         {
	         "id": "<INT: CATEGORY ID>",
	         "category": "<STRING: CATEGORY NAME>"
	         }
	         "..."
	     ]

     }
}
```


### Login
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
          "name": "<STRING: USER NAME>",
	  "email": "<STRING: EMAIL>",
          "session_token": "<STRING: SESSION TOKEN>", 
          "session_expiration": "<STRING: DATE-TIME>", 
          "update_token": "<STRING: UPDATE TOKEN>"
        }
}
```

### Update Session
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
          "id": "<STRING: USER_ID>",
	  "name": "<STRING: USER NAME>",
	  "email": "<STRING: EMAIL>",
          "session_token": "<STRING: SESSION TOKEN>", 
          "session_expiration": "<STRING: DATE-TIME>", 
          "update_token": "<STRING: UPDATE TOKEN>"
        }
}
```

### Get Categories
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

### Get Photos Of Category
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
  "data": [
         {
          "category": "<STRING: CATEGORY NAME>",
          "type": "quote",
          "quote": "<STRING: QUOTE STRING>",
          "author": "<STRING: AUTHOR NAME>"
        },
	"..."
        {
          "id": "<INT: PHOTO ID>", 
          "type": "photo",
          "category": "<STRING: CATEGORY NAME>",
          "source": "<STRING: PHOTO URL>",
          "author": "<STRING: PHOTOGRAPHER NAME> - Uploaded to Pexel Photos"
        },
        {
          "id": "<INT: PHOTO ID>", 
          "type": "photo",
          "category": "<STRING: CATEGORY NAME>",
          "source": "<STRING: PHOTO URL>",
          "author": "<STRING: PHOTOGRAPHER NAME> - Uploaded to Pexel Photos"
        },
        "..."
    ]
}
```

### Get Photos User Will Like
`POST` `/api/data/<int:user_id>/`
```json
Request 

{ 
    "authorization": "<STRING: SESSION TOKEN>"
}
```

```json
Response

{
  "success": true, 
  "data":  [
        {
          "category": "<STRING: CATEGORY NAME>",
	  "type": "quote",
          "source": "<STRING: QUOTE STRING>",
          "author": "<STRING: AUTHOR NAME>"
        },
            "… (as many as user’s liked categories)"
        {
          "id": "<INT: PHOTO ID>", 
          "type": "photo",
          "category": "<STRING: CATEGORY NAME>",
          "source": "<STRING: PHOTO URL>",
          "author": "<STRING: PHOTOGRAPHER NAME> - Uploaded to Pexel Photos"
        },
        {
          "id": "<INT: PHOTO ID>", 
          "type": "photo",
          "category": "<STRING: CATEGORY NAME>",
          "source": "<STRING: PHOTO URL>",
          "author": "<STRING: PHOTOGRAPHER NAME> - Uploaded to Pexel Photos"
        },
      "..."
    ]
}
```

### Add Category to User Preferences
`POST` `/api/<int:user_id>/category/`
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
  "data": [
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
            "..."
          ]
        }
    ]
}
```

### Remove Category from User Preferences
`DELETE` `/api/<int:user_id>/category/`
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
  "data": [
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
            "..."
          ]
        }
    ]
}
```

### Get Themed Quote
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
          "type": "quote",
          "source": "<STRING: QUOTE>",
          "author": "<STRING: AUTHOR>
        }
}
```

### Get Random Quote for User
`POST` `/api/<int:user_id>/quote/`
```json
Request 

{ 
    "authorization": "<STRING: SESSION TOKEN>"
}
```

```json
Response

{
  "success": true, 
  "data": 
        {
          "category": "<STRING: QUOTE THEME>",
          "type": "quote",
          "source": "<STRING: QUOTE>",
          "author": "<STRING: AUTHOR>"

        }
}
```

# Extra Cool Stuff
* Multithreading
   * Creates a Daemon Thread to automatically update the photos in the data table every hour
   * This prevents causing the main thread to sleep and helps mitigate deadlocking during updating
* mySQL server using Cloud SQL and Google Cloud Run to Deploy Containers
* Authentication and Encryption and HTTPS Secured
