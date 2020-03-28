REST API for Voice Assistant
===

##### REST path

+ [/events/ GET](##get-events)
+ [/events/ POST](##creating-event)
+ [/events/id/ GET](##get-event)
+ [/events/id/ PUT](##updating-event)
+ [/events/id/ DELETE](##delete-event)
+ [/tasks/ GET](##get-tasks)
+ [/tasks/ POST](##creating-task)
+ [/tasks/id/ GET](##get-task)
+ [/tasks/id/ PUT](##updating-task)
+ [/tasks/id/ DELETE](##delete-task)
+ [/register/ POST](##creating-new-user)
+ [/auth/ POST](##login)

##### Endpoints that doesn't require authentication:
+ /register/ POST
+ /auth/POST

##### Authentication
To obtain authentication you need to add a specific header to your request. It should look like this:
```JSON
{
    "Authorization": "Token <your token>"
}
```
## Creating new user
```/register/ POST```

JSON params
```JSON
{
    "username": "Must be unique, Required, 150 characters or fewer.",
    "email": "Required, must be valid email address",
    "password": "Required."
}
```
Possible responses:

+ *status code 400* : not valid email format
+ *status code 409* : username exists, or some field is missing
+ *status code 201*: user created


## Login
```/auth/ POST```

JSON params
```JSON
{
    "username": "your username",
    "password": "your password"
}
```
Possible responses:

+ *status code 400* : invalid credentials

+ *status code 200* : success
```JSON
{
    "token": "<your access token>"
}
```

## Creating event
```/events/ POST```

JSON params
```JSON
{
    "event_name": "Max lenght: 100",
    "date": "Default: now"
}
```
Possible responses:
+ *status code 401* : not authenticated

+ *status code 400* : event_name is required

+ *status code 201* : event created
```JSON
{
    "username": "Your username",
    "event_name": "some name",
    "date": "In ISO 8601 format",
    "id": "Integer"
}
```
## Get events
```/events/ GET```


Possible responses:

+ *status code 401* : not authenticated

+ *status code 200* : list of your events
```JSON
[
    {
        "username": "Your username",
        "event_name": "some name",
        "date": "In ISO 8601 format",
        "id": "Integer"
    },
    ...
]
```

## Get event
```/events/id/ GET```


Possible responses:

+ *status code 403* : event belongs to other user

+ *status code 401* : not authenticated

+ *status code 200* : your event
```JSON
{
    "username": "Your username",
    "event_name": "some name",
    "date": "In ISO 8601 format",
    "id": "Integer"
}
```

## Delete event
```/events/id/ DELETE```

Possible responses:

+ *status code 403* : event belongs to other user

+ *status code 401* : not authenticated

+ *status code 204* : event deleted


## Updating event
```/events/id/ PUT```

JSON params
```JSON
{
    "event_name": "Required new name",
    "date": "Default: old date"
}
```
Possible responses:
+ *status code 401* : not authenticated

+ *status code 400* : event_name is required

+ *status code 200* : event updated
```JSON
{
    "username": "Your username",
    "event_name": "some name",
    "date": "In ISO 8601 format",
    "id": "Integer"
}
```

## Creating task
```/tasks/ POST```

JSON params
```JSON
{
    "task_name": "Max lenght: 100",
    "date": "Default: now",
    "is_done": "Default: False"
}
```
Possible responses:
+ *status code 401* : not authenticated

+ *status code 400* : task_name is required

+ *status code 201* : task created
```JSON
{
    "username": "Your username",
    "task_name": "some name",
    "date": "In ISO 8601 format",
    "id": "Integer",
    "is_done": "True/False"
}
```
## Get tasks
```/tasks/ GET```


Possible responses:

+ *status code 401* : not authenticated

+ *status code 200* : list of your tasks
```JSON
[
    {
        "username": "Your username",
        "task_name": "some name",
        "date": "In ISO 8601 format",
        "id": "Integer",
        "is_done": "Boolean"
    },
    ...
]
```

## Get task
```/tasks/id/ GET```


Possible responses:

+ *status code 403* : task belongs to other user

+ *status code 401* : not authenticated

+ *status code 200* : your task
```JSON
{
    "username": "Your username",
    "task_name": "some name",
    "date": "In ISO 8601 format",
    "id": "Integer",
    "is_done": "Boolean"
}
```

## Delete task
```/tasks/id/ DELETE```

Possible responses:

+ *status code 403* : task belongs to other user

+ *status code 401* : not authenticated

+ *status code 204* : task deleted


## Updating task
```/tasks/id/ PUT```

JSON params
```JSON
{ 
    "task_name": "Max lenght: 100",
    "date": "Default: old date",
    "is_done": "Default: old is_done"
}
```
Possible responses:
+ *status code 401* : not authenticated

+ *status code 400* : task_name is required

+ *status code 200* : task updated
```JSON
{
    "username": "Your username",
    "task_name": "some name",
    "date": "In ISO 8601 format",
    "id": "Integer",
    "is_done": "Boolean"
}
```