# API Documentation
Generated on: 2022-12-08 at 16:26:30

- [GET /api/](#get-api)
- [POST /api/auth/register](#post-apiauthregister)
- [POST /api/auth/login](#post-apiauthlogin)
- [GET /api/users](#get-apiusers)
- [GET /api/users/me](#get-apiusersme)
- [GET /api/users/1](#get-apiusers1)
- [DELETE /api/users/3](#delete-apiusers3)
- [POST /api/chats](#post-apichats)
- [GET /api/chats](#get-apichats)
- [GET /api/chats/1](#get-apichats1)
- [POST /api/chats/1/messages](#post-apichats1messages)
- [GET /api/chats/messages/latest](#get-apichatsmessageslatest)
- [GET /api/chats/1/messages](#get-apichats1messages)
- [DELETE /api/chats/1](#delete-apichats1)
- [GET /api/roles](#get-apiroles)
- [GET /api/roles/1](#get-apiroles1)
- [POST /api/roles](#post-apiroles)
- [POST /api/roles/3](#post-apiroles3)
- [DELETE /api/roles/3](#delete-apiroles3)
- [POST /api/listings](#post-apilistings)
- [POST /api/listings](#post-apilistings)
- [POST /api/listings](#post-apilistings)
- [POST /api/listings](#post-apilistings)
- [POST /api/listings](#post-apilistings)
- [POST /api/listings](#post-apilistings)
- [POST /api/listings/1](#post-apilistings1)
- [POST /api/listings/1](#post-apilistings1)
- [GET /api/listings/](#get-apilistings)
- [GET /api/listings/?type=donor](#get-apilistingstypedonor)
- [GET /api/listings/?type=receiver](#get-apilistingstypereceiver)
- [GET /api/listings/1](#get-apilistings1)
- [GET /api/listings/4/matches](#get-apilistings4matches)
- [GET /api/listings/5/matches](#get-apilistings5matches)
- [GET /api/listings/6/matches](#get-apilistings6matches)
- [DELETE /api/listings/2](#delete-apilistings2)


## GET /api/
Information about the server, such as the version or the OS.
Useful to check if the server is up, or to check if it is running
the latest version.

### Response
```json
{
  "version": "5e495f1",
  "time": 1670509590.026772,
  "datetime": "2022-12-08 15:26:30.026772",
  "software": {
    "flask": "2.2.2",
    "python": "3.10.7",
    "system": {
      "name": "Ubuntu 22.10",
      "platform": "Linux",
      "release": "5.15.79.1-microsoft-standard-WSL2",
      "arch": "x86_64"
    }
  }
}
```

**Status:** 200

## POST /api/auth/register
Register a new user, response should be the same as login, so no need to
login after registering.

### Request
```json
{
  "email": "user19@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "token": "1-1-87b5862e47eef0f0a13ffbc5ea6f86f95b03fd8fe34b591f2ad4331ed3bd05c2",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 1,
    "created_at": "2022-12-08 15:26:30.259557",
    "updated_at": null,
    "email": "user19@email.com",
    "phone_number": "01 23 45 67 89",
    "role": {
      "id": 1,
      "can_edit_users": true,
      "can_edit_hospitals": true,
      "can_edit_listings": true,
      "can_edit_staff": true,
      "can_edit_roles": true,
      "can_edit_persons": true,
      "name": "admin"
    }
  }
}
```

**Status:** 201
### Request
```json
{
  "email": "user19@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "msg": "email \"user19@email.com\" is already taken."
}
```

**Status:** 422

## POST /api/auth/login
Login and get a token.

### Request
```json
{
  "email": "user19@email.com",
  "password": "password"
}
```

### Response
```json
{
  "token": "3-1-7ce49ae41b061f88bfafc27a3f0b638ee5e9d479bdb0e43435f7439d96662cec",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 1,
    "created_at": "2022-12-08 15:26:30.259557",
    "updated_at": null,
    "email": "user19@email.com",
    "phone_number": "01 23 45 67 89",
    "role": {
      "id": 1,
      "can_edit_users": true,
      "can_edit_hospitals": true,
      "can_edit_listings": true,
      "can_edit_staff": true,
      "can_edit_roles": true,
      "can_edit_persons": true,
      "name": "admin"
    }
  }
}
```

**Status:** 200
### Request
```json
{
  "email": "user@email.com",
  "password": "not-the-password"
}
```

### Response
```json
{
  "msg": "User not found"
}
```

**Status:** 422
### Request
```json
{
  "email": "user19@email.com",
  "password": "not-the-password"
}
```

### Response
```json
{
  "msg": "Password mismatch"
}
```

**Status:** 422

## GET /api/users
List all users

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 1,
    "created_at": "2022-12-08 15:26:30.259557",
    "updated_at": null,
    "email": "user19@email.com",
    "phone_number": "01 23 45 67 89",
    "role": {
      "id": 1,
      "can_edit_users": true,
      "can_edit_hospitals": true,
      "can_edit_listings": true,
      "can_edit_staff": true,
      "can_edit_roles": true,
      "can_edit_persons": true,
      "name": "admin"
    }
  },
  {
    "firstname": null,
    "lastname": null,
    "id": 2,
    "created_at": "2022-12-08 15:26:30.655590",
    "updated_at": null,
    "email": "user803@email.com",
    "phone_number": null,
    "role": {
      "id": 1,
      "can_edit_users": true,
      "can_edit_hospitals": true,
      "can_edit_listings": true,
      "can_edit_staff": true,
      "can_edit_roles": true,
      "can_edit_persons": true,
      "name": "admin"
    }
  },
  {
    "firstname": null,
    "lastname": null,
    "id": 3,
    "created_at": "2022-12-08 15:26:31.397897",
    "updated_at": "2022-12-08 15:26:31.406775",
    "email": "admin@localhost",
    "phone_number": null,
    "role": {
      "id": 1,
      "can_edit_users": true,
      "can_edit_hospitals": true,
      "can_edit_listings": true,
      "can_edit_staff": true,
      "can_edit_roles": true,
      "can_edit_persons": true,
      "name": "admin"
    }
  }
]
```

**Status:** 200

## GET /api/users/me
Get info about the current user

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "firstname": null,
  "lastname": null,
  "id": 3,
  "created_at": "2022-12-08 15:26:31.397897",
  "updated_at": "2022-12-08 15:26:31.406775",
  "email": "admin@localhost",
  "phone_number": null,
  "role": {
    "id": 1,
    "can_edit_users": true,
    "can_edit_hospitals": true,
    "can_edit_listings": true,
    "can_edit_staff": true,
    "can_edit_roles": true,
    "can_edit_persons": true,
    "name": "admin"
  }
}
```

**Status:** 200

## GET /api/users/1
Get info about a specific user

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "firstname": "prenom",
  "lastname": "nom",
  "id": 1,
  "created_at": "2022-12-08 15:26:30.259557",
  "updated_at": null,
  "email": "user19@email.com",
  "phone_number": "01 23 45 67 89",
  "role": {
    "id": 1,
    "can_edit_users": true,
    "can_edit_hospitals": true,
    "can_edit_listings": true,
    "can_edit_staff": true,
    "can_edit_roles": true,
    "can_edit_persons": true,
    "name": "admin"
  }
}
```

**Status:** 200

## DELETE /api/users/3
Delete a user

> :police_car: This request requires specific permissions. An user must be authenticated via a token and their role must have the permissions edit_users to access this route.
### Response
**Status:** 204

## POST /api/chats
Create a new chat

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "name": "Chat name",
  "users_ids": [
    1,
    2
  ]
}
```

### Response
```json
{
  "id": 1,
  "created_at": "2022-12-08 15:26:31.511091",
  "updated_at": null,
  "name": "Chat name",
  "users": [
    {
      "firstname": "prenom",
      "lastname": "nom",
      "id": 1,
      "created_at": "2022-12-08 15:26:30.259557",
      "updated_at": null,
      "email": "user19@email.com",
      "phone_number": "01 23 45 67 89",
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    },
    {
      "firstname": null,
      "lastname": null,
      "id": 2,
      "created_at": "2022-12-08 15:26:30.655590",
      "updated_at": null,
      "email": "user803@email.com",
      "phone_number": null,
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    },
    {
      "firstname": null,
      "lastname": null,
      "id": 3,
      "created_at": "2022-12-08 15:26:31.491018",
      "updated_at": "2022-12-08 15:26:31.498817",
      "email": "admin@localhost",
      "phone_number": null,
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    }
  ],
  "creator": {
    "firstname": null,
    "lastname": null,
    "id": 3,
    "created_at": "2022-12-08 15:26:31.491018",
    "updated_at": "2022-12-08 15:26:31.498817",
    "email": "admin@localhost",
    "phone_number": null,
    "role": {
      "id": 1,
      "can_edit_users": true,
      "can_edit_hospitals": true,
      "can_edit_listings": true,
      "can_edit_staff": true,
      "can_edit_roles": true,
      "can_edit_persons": true,
      "name": "admin"
    }
  }
}
```

**Status:** 200

## GET /api/chats
Get all the chats the current user is part of

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "id": 1,
    "created_at": "2022-12-08 15:26:31.511091",
    "updated_at": null,
    "name": "Chat name",
    "users": [
      {
        "firstname": "prenom",
        "lastname": "nom",
        "id": 1,
        "created_at": "2022-12-08 15:26:30.259557",
        "updated_at": null,
        "email": "user19@email.com",
        "phone_number": "01 23 45 67 89",
        "role": {
          "id": 1,
          "can_edit_users": true,
          "can_edit_hospitals": true,
          "can_edit_listings": true,
          "can_edit_staff": true,
          "can_edit_roles": true,
          "can_edit_persons": true,
          "name": "admin"
        }
      },
      {
        "firstname": null,
        "lastname": null,
        "id": 2,
        "created_at": "2022-12-08 15:26:30.655590",
        "updated_at": null,
        "email": "user803@email.com",
        "phone_number": null,
        "role": {
          "id": 1,
          "can_edit_users": true,
          "can_edit_hospitals": true,
          "can_edit_listings": true,
          "can_edit_staff": true,
          "can_edit_roles": true,
          "can_edit_persons": true,
          "name": "admin"
        }
      },
      {
        "firstname": null,
        "lastname": null,
        "id": 3,
        "created_at": "2022-12-08 15:26:31.491018",
        "updated_at": "2022-12-08 15:26:31.498817",
        "email": "admin@localhost",
        "phone_number": null,
        "role": {
          "id": 1,
          "can_edit_users": true,
          "can_edit_hospitals": true,
          "can_edit_listings": true,
          "can_edit_staff": true,
          "can_edit_roles": true,
          "can_edit_persons": true,
          "name": "admin"
        }
      }
    ],
    "creator": {
      "firstname": null,
      "lastname": null,
      "id": 3,
      "created_at": "2022-12-08 15:26:31.491018",
      "updated_at": "2022-12-08 15:26:31.498817",
      "email": "admin@localhost",
      "phone_number": null,
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    }
  }
]
```

**Status:** 200

## GET /api/chats/1
Get a specific chat

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "id": 1,
  "created_at": "2022-12-08 15:26:31.511091",
  "updated_at": null,
  "name": "Chat name",
  "users": [
    {
      "firstname": "prenom",
      "lastname": "nom",
      "id": 1,
      "created_at": "2022-12-08 15:26:30.259557",
      "updated_at": null,
      "email": "user19@email.com",
      "phone_number": "01 23 45 67 89",
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    },
    {
      "firstname": null,
      "lastname": null,
      "id": 2,
      "created_at": "2022-12-08 15:26:30.655590",
      "updated_at": null,
      "email": "user803@email.com",
      "phone_number": null,
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    },
    {
      "firstname": null,
      "lastname": null,
      "id": 3,
      "created_at": "2022-12-08 15:26:31.491018",
      "updated_at": "2022-12-08 15:26:31.498817",
      "email": "admin@localhost",
      "phone_number": null,
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    }
  ],
  "creator": {
    "firstname": null,
    "lastname": null,
    "id": 3,
    "created_at": "2022-12-08 15:26:31.491018",
    "updated_at": "2022-12-08 15:26:31.498817",
    "email": "admin@localhost",
    "phone_number": null,
    "role": {
      "id": 1,
      "can_edit_users": true,
      "can_edit_hospitals": true,
      "can_edit_listings": true,
      "can_edit_staff": true,
      "can_edit_roles": true,
      "can_edit_persons": true,
      "name": "admin"
    }
  }
}
```

**Status:** 200

## POST /api/chats/1/messages
Send a message

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "content": "Hello world!"
}
```

### Response
```json
{
  "content": "Hello world!",
  "chat": {
    "id": 1,
    "created_at": "2022-12-08 15:26:31.511091",
    "updated_at": null,
    "name": "Chat name",
    "users": [
      {
        "firstname": "prenom",
        "lastname": "nom",
        "id": 1,
        "created_at": "2022-12-08 15:26:30.259557",
        "updated_at": null,
        "email": "user19@email.com",
        "phone_number": "01 23 45 67 89",
        "role": {
          "id": 1,
          "can_edit_users": true,
          "can_edit_hospitals": true,
          "can_edit_listings": true,
          "can_edit_staff": true,
          "can_edit_roles": true,
          "can_edit_persons": true,
          "name": "admin"
        }
      },
      {
        "firstname": null,
        "lastname": null,
        "id": 2,
        "created_at": "2022-12-08 15:26:30.655590",
        "updated_at": null,
        "email": "user803@email.com",
        "phone_number": null,
        "role": {
          "id": 1,
          "can_edit_users": true,
          "can_edit_hospitals": true,
          "can_edit_listings": true,
          "can_edit_staff": true,
          "can_edit_roles": true,
          "can_edit_persons": true,
          "name": "admin"
        }
      },
      {
        "firstname": null,
        "lastname": null,
        "id": 3,
        "created_at": "2022-12-08 15:26:31.491018",
        "updated_at": "2022-12-08 15:26:31.498817",
        "email": "admin@localhost",
        "phone_number": null,
        "role": {
          "id": 1,
          "can_edit_users": true,
          "can_edit_hospitals": true,
          "can_edit_listings": true,
          "can_edit_staff": true,
          "can_edit_roles": true,
          "can_edit_persons": true,
          "name": "admin"
        }
      }
    ],
    "creator": {
      "firstname": null,
      "lastname": null,
      "id": 3,
      "created_at": "2022-12-08 15:26:31.491018",
      "updated_at": "2022-12-08 15:26:31.498817",
      "email": "admin@localhost",
      "phone_number": null,
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    }
  },
  "sender": {
    "firstname": null,
    "lastname": null,
    "id": 3,
    "created_at": "2022-12-08 15:26:31.491018",
    "updated_at": "2022-12-08 15:26:31.498817",
    "email": "admin@localhost",
    "phone_number": null,
    "role": {
      "id": 1,
      "can_edit_users": true,
      "can_edit_hospitals": true,
      "can_edit_listings": true,
      "can_edit_staff": true,
      "can_edit_roles": true,
      "can_edit_persons": true,
      "name": "admin"
    }
  },
  "id": 1,
  "created_at": "2022-12-08 15:26:31.569125"
}
```

**Status:** 200

## GET /api/chats/messages/latest
Get all chats the current user is part of and the last message of each

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "content": "Hello world!",
    "chat": {
      "id": 1,
      "created_at": "2022-12-08 15:26:31.511091",
      "updated_at": null,
      "name": "Chat name",
      "users": [
        {
          "firstname": "prenom",
          "lastname": "nom",
          "id": 1,
          "created_at": "2022-12-08 15:26:30.259557",
          "updated_at": null,
          "email": "user19@email.com",
          "phone_number": "01 23 45 67 89",
          "role": {
            "id": 1,
            "can_edit_users": true,
            "can_edit_hospitals": true,
            "can_edit_listings": true,
            "can_edit_staff": true,
            "can_edit_roles": true,
            "can_edit_persons": true,
            "name": "admin"
          }
        },
        {
          "firstname": null,
          "lastname": null,
          "id": 2,
          "created_at": "2022-12-08 15:26:30.655590",
          "updated_at": null,
          "email": "user803@email.com",
          "phone_number": null,
          "role": {
            "id": 1,
            "can_edit_users": true,
            "can_edit_hospitals": true,
            "can_edit_listings": true,
            "can_edit_staff": true,
            "can_edit_roles": true,
            "can_edit_persons": true,
            "name": "admin"
          }
        },
        {
          "firstname": null,
          "lastname": null,
          "id": 3,
          "created_at": "2022-12-08 15:26:31.491018",
          "updated_at": "2022-12-08 15:26:31.498817",
          "email": "admin@localhost",
          "phone_number": null,
          "role": {
            "id": 1,
            "can_edit_users": true,
            "can_edit_hospitals": true,
            "can_edit_listings": true,
            "can_edit_staff": true,
            "can_edit_roles": true,
            "can_edit_persons": true,
            "name": "admin"
          }
        }
      ],
      "creator": {
        "firstname": null,
        "lastname": null,
        "id": 3,
        "created_at": "2022-12-08 15:26:31.491018",
        "updated_at": "2022-12-08 15:26:31.498817",
        "email": "admin@localhost",
        "phone_number": null,
        "role": {
          "id": 1,
          "can_edit_users": true,
          "can_edit_hospitals": true,
          "can_edit_listings": true,
          "can_edit_staff": true,
          "can_edit_roles": true,
          "can_edit_persons": true,
          "name": "admin"
        }
      }
    },
    "sender": {
      "firstname": null,
      "lastname": null,
      "id": 3,
      "created_at": "2022-12-08 15:26:31.491018",
      "updated_at": "2022-12-08 15:26:31.498817",
      "email": "admin@localhost",
      "phone_number": null,
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    },
    "id": 1,
    "created_at": "2022-12-08 15:26:31.569125"
  }
]
```

**Status:** 200

## GET /api/chats/1/messages
Get all messages for a specific chat

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "content": "Hello world!",
    "chat": {
      "id": 1,
      "created_at": "2022-12-08 15:26:31.511091",
      "updated_at": null,
      "name": "Chat name",
      "users": [
        {
          "firstname": "prenom",
          "lastname": "nom",
          "id": 1,
          "created_at": "2022-12-08 15:26:30.259557",
          "updated_at": null,
          "email": "user19@email.com",
          "phone_number": "01 23 45 67 89",
          "role": {
            "id": 1,
            "can_edit_users": true,
            "can_edit_hospitals": true,
            "can_edit_listings": true,
            "can_edit_staff": true,
            "can_edit_roles": true,
            "can_edit_persons": true,
            "name": "admin"
          }
        },
        {
          "firstname": null,
          "lastname": null,
          "id": 2,
          "created_at": "2022-12-08 15:26:30.655590",
          "updated_at": null,
          "email": "user803@email.com",
          "phone_number": null,
          "role": {
            "id": 1,
            "can_edit_users": true,
            "can_edit_hospitals": true,
            "can_edit_listings": true,
            "can_edit_staff": true,
            "can_edit_roles": true,
            "can_edit_persons": true,
            "name": "admin"
          }
        },
        {
          "firstname": null,
          "lastname": null,
          "id": 3,
          "created_at": "2022-12-08 15:26:31.491018",
          "updated_at": "2022-12-08 15:26:31.498817",
          "email": "admin@localhost",
          "phone_number": null,
          "role": {
            "id": 1,
            "can_edit_users": true,
            "can_edit_hospitals": true,
            "can_edit_listings": true,
            "can_edit_staff": true,
            "can_edit_roles": true,
            "can_edit_persons": true,
            "name": "admin"
          }
        }
      ],
      "creator": {
        "firstname": null,
        "lastname": null,
        "id": 3,
        "created_at": "2022-12-08 15:26:31.491018",
        "updated_at": "2022-12-08 15:26:31.498817",
        "email": "admin@localhost",
        "phone_number": null,
        "role": {
          "id": 1,
          "can_edit_users": true,
          "can_edit_hospitals": true,
          "can_edit_listings": true,
          "can_edit_staff": true,
          "can_edit_roles": true,
          "can_edit_persons": true,
          "name": "admin"
        }
      }
    },
    "sender": {
      "firstname": null,
      "lastname": null,
      "id": 3,
      "created_at": "2022-12-08 15:26:31.491018",
      "updated_at": "2022-12-08 15:26:31.498817",
      "email": "admin@localhost",
      "phone_number": null,
      "role": {
        "id": 1,
        "can_edit_users": true,
        "can_edit_hospitals": true,
        "can_edit_listings": true,
        "can_edit_staff": true,
        "can_edit_roles": true,
        "can_edit_persons": true,
        "name": "admin"
      }
    },
    "id": 1,
    "created_at": "2022-12-08 15:26:31.569125"
  }
]
```

**Status:** 200

## DELETE /api/chats/1
Delete a chat

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 204

## GET /api/roles
Lists all user roles

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "id": 1,
    "can_edit_users": true,
    "can_edit_hospitals": true,
    "can_edit_listings": true,
    "can_edit_staff": true,
    "can_edit_roles": true,
    "can_edit_persons": true,
    "name": "admin"
  },
  {
    "id": 2,
    "can_edit_users": false,
    "can_edit_hospitals": false,
    "can_edit_listings": false,
    "can_edit_staff": false,
    "can_edit_roles": false,
    "can_edit_persons": false,
    "name": "default"
  }
]
```

**Status:** 200

## GET /api/roles/1
Get a specific role

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "id": 1,
  "can_edit_users": true,
  "can_edit_hospitals": true,
  "can_edit_listings": true,
  "can_edit_staff": true,
  "can_edit_roles": true,
  "can_edit_persons": true,
  "name": "admin"
}
```

**Status:** 200

## POST /api/roles
Create a new role

> :police_car: This request requires specific permissions. An user must be authenticated via a token and their role must have the permissions edit_roles to access this route.
### Request
```json
{
  "name": "New role",
  "can_edit_users": false,
  "can_edit_hospitals": false,
  "can_edit_listings": false,
  "can_edit_staff": false,
  "can_edit_roles": false,
  "can_edit_persons": false
}
```

### Response
```json
{
  "id": 3,
  "can_edit_users": false,
  "can_edit_hospitals": false,
  "can_edit_listings": false,
  "can_edit_staff": false,
  "can_edit_roles": false,
  "can_edit_persons": false,
  "name": "New role"
}
```

**Status:** 200

## POST /api/roles/3
Update a role

> :police_car: This request requires specific permissions. An user must be authenticated via a token and their role must have the permissions edit_roles to access this route.
### Request
```json
{
  "name": "Updated role"
}
```

### Response
```json
{
  "id": 3,
  "can_edit_users": false,
  "can_edit_hospitals": false,
  "can_edit_listings": false,
  "can_edit_staff": false,
  "can_edit_roles": false,
  "can_edit_persons": false,
  "name": "Updated role"
}
```

**Status:** 200

## DELETE /api/roles/3
Delete a role

> :police_car: This request requires specific permissions. An user must be authenticated via a token and their role must have the permissions edit_roles to access this route.
### Response
**Status:** 204

## POST /api/listings
Create a receiver listing for a liver, creating the Person and Organ in
one go

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "type": "RECEIVER",
  "person": {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+33123456789",
    "gender": "MALE",
    "birth_date": "1990-02-10",
    "abo": "A",
    "rhesus": "+"
  },
  "organ_type": "LIVER",
  "organ": {
    "tumors_count": 2,
    "biggest_tumor_size": 10,
    "alpha_fetoprotein": 10
  }
}
```

### Response
```json
{
  "id": 1,
  "notes": null,
  "type": "RECEIVER",
  "organ_type": "LIVER",
  "start_date": null,
  "end_date": null,
  "person": {
    "id": 1,
    "created_at": "2022-12-08 15:26:31.731578",
    "updated_at": null,
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "abo": "A",
    "rhesus": "Rhesus.POSITIVE",
    "user": null
  },
  "organ": {
    "id": 1,
    "tumors_count": 2,
    "biggest_tumor_size": 10,
    "alpha_fetoprotein": 10,
    "listing_id": 1
  },
  "hospital": null
}
```

**Status:** 200

## POST /api/listings
Create a receiver listing for a lung, creating the Person and Organ in
one go
- `diagnosis_group` can be A, B, C, or D
- `detailed_diagnosis` can be one of the following: BRONCHIECTASIS,
EISENMENGER, BRONCHIOLITIS, LAM, or SARCOIDOSIS
- `body_mass_index` for a normal person is expected to be between 18.5 and
25
- `pulmonary_artery_systolic` is expected to be between 17 and 20, > 30 is
considered critical
- `carbon_dioxide_partial_pressure` is expected to be between 35 and 40
- `pulmonary_capilary_wedge_pressure` is expected to be between 8 and 12,
\> 20 is considered critical
- `creatinine` is expected to be between 7 and 13

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "type": "RECEIVER",
  "person": {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+33123456789",
    "gender": "MALE",
    "birth_date": "1990-02-10",
    "abo": "A",
    "rhesus": "+"
  },
  "organ_type": "LUNG",
  "organ": {
    "diagnosis_group": "A",
    "detailed_diagnosis": "LAM",
    "body_mass_index": 17.9,
    "diabetes": false,
    "assistance_required": false,
    "pulmonary_function_percentage": 0.85,
    "pulmonary_artery_systolic": 25.2,
    "oxygen_requirement": 0.5,
    "six_minutes_walk_distance_over_150_feet": true,
    "continuous_mech_ventilation": true,
    "carbon_dioxide_partial_pressure": 36.3,
    "carbon_dioxide_partial_pressure_15_percent_increase": false,
    "activities_of_daily_life_required": false,
    "pulmonary_capilary_wedge_pressure": 9.2,
    "creatinine": 10.2
  }
}
```

### Response
```json
{
  "id": 2,
  "notes": null,
  "type": "RECEIVER",
  "organ_type": "LUNG",
  "start_date": null,
  "end_date": null,
  "person": {
    "id": 2,
    "created_at": "2022-12-08 15:26:31.759343",
    "updated_at": null,
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "abo": "A",
    "rhesus": "Rhesus.POSITIVE",
    "user": null
  },
  "organ": {
    "id": 1,
    "diagnosis_group": "A",
    "detailed_diagnosis": "LAM",
    "body_mass_index": 17.9,
    "diabetes": false,
    "assistance_required": false,
    "pulmonary_function_percentage": 0.85,
    "pulmonary_artery_systolic": 25.2,
    "oxygen_requirement": 0.5,
    "six_minutes_walk_distance_over_150_feet": true,
    "continuous_mech_ventilation": true,
    "carbon_dioxide_partial_pressure": 36.3,
    "carbon_dioxide_partial_pressure_15_percent_increase": false,
    "creatinine": 10.2,
    "activities_of_daily_life_required": false,
    "pulmonary_capilary_wedge_pressure": 9.2,
    "listing_id": 2
  },
  "hospital": null
}
```

**Status:** 200

## POST /api/listings
Create a receiver listing for a kidney, creating the Person in one go

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "type": "RECEIVER",
  "person": {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+33123456789",
    "gender": "MALE",
    "birth_date": "1990-02-10",
    "abo": "A",
    "rhesus": "+"
  },
  "organ": {
    "is_under_dialysis": true,
    "is_retransplantation": false,
    "dialysis_start_date": "2022-12-12",
    "arf_date": "2022-12-12",
    "date_transplantation": "2022-12-12",
    "re_registration_date": "2022-12-12",
    "A": 1.2,
    "B": 1.3,
    "DR": 1.4,
    "DQ": 1.5
  },
  "organ_type": "KIDNEY"
}
```

### Response
```json
{
  "id": 3,
  "notes": null,
  "type": "RECEIVER",
  "organ_type": "KIDNEY",
  "start_date": null,
  "end_date": null,
  "person": {
    "id": 3,
    "created_at": "2022-12-08 15:26:31.788394",
    "updated_at": null,
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "abo": "A",
    "rhesus": "Rhesus.POSITIVE",
    "user": null
  },
  "organ": {
    "id": 1,
    "is_under_dialysis": true,
    "is_retransplantation": false,
    "dialysis_start_date": "2022-12-12",
    "dialysis_end_date": null,
    "arf_date": "2022-12-12",
    "date_transplantation": "2022-12-12",
    "re_registration_date": "2022-12-12",
    "A": 1.2,
    "B": 1.3,
    "DR": 1.4,
    "DQ": 1.5,
    "listing_id": 3
  },
  "hospital": null
}
```

**Status:** 200

## POST /api/listings
Create a donor listing for a liver, creating the Person in one go

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "type": "DONOR",
  "person": {
    "first_name": "Johnatan",
    "last_name": "Joeystarr",
    "phone_number": "+33123456789",
    "gender": "MALE",
    "birth_date": "1990-02-10",
    "abo": "A",
    "rhesus": "+"
  },
  "organ_type": "LIVER"
}
```

### Response
```json
{
  "id": 4,
  "notes": null,
  "type": "DONOR",
  "organ_type": "LIVER",
  "start_date": null,
  "end_date": null,
  "person": {
    "id": 4,
    "created_at": "2022-12-08 15:26:31.817156",
    "updated_at": null,
    "first_name": "Johnatan",
    "last_name": "Joeystarr",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "abo": "A",
    "rhesus": "Rhesus.POSITIVE",
    "user": null
  },
  "organ": null,
  "hospital": null
}
```

**Status:** 200

## POST /api/listings
Create a donor listing for a kidney, creating the Person in one go

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "type": "DONOR",
  "person": {
    "first_name": "Johnatan",
    "last_name": "Joeystarr",
    "phone_number": "+33123456789",
    "gender": "MALE",
    "birth_date": "1990-02-10",
    "abo": "A",
    "rhesus": "+"
  },
  "organ_type": "KIDNEY"
}
```

### Response
```json
{
  "id": 5,
  "notes": null,
  "type": "DONOR",
  "organ_type": "KIDNEY",
  "start_date": null,
  "end_date": null,
  "person": {
    "id": 5,
    "created_at": "2022-12-08 15:26:31.842991",
    "updated_at": null,
    "first_name": "Johnatan",
    "last_name": "Joeystarr",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "abo": "A",
    "rhesus": "Rhesus.POSITIVE",
    "user": null
  },
  "organ": null,
  "hospital": null
}
```

**Status:** 200

## POST /api/listings
Create a donor listing for a lung, creating the Person in one go

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "type": "DONOR",
  "person": {
    "first_name": "Johnatan",
    "last_name": "Joeystarr",
    "phone_number": "+33123456789",
    "gender": "MALE",
    "birth_date": "1990-02-10",
    "abo": "A",
    "rhesus": "+"
  },
  "organ_type": "LUNG"
}
```

### Response
```json
{
  "id": 6,
  "notes": null,
  "type": "DONOR",
  "organ_type": "LUNG",
  "start_date": null,
  "end_date": null,
  "person": {
    "id": 6,
    "created_at": "2022-12-08 15:26:31.878462",
    "updated_at": null,
    "first_name": "Johnatan",
    "last_name": "Joeystarr",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "abo": "A",
    "rhesus": "Rhesus.POSITIVE",
    "user": null
  },
  "organ": null,
  "hospital": null
}
```

**Status:** 200

## POST /api/listings/1
Update a listing

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "start_date": "2020-02-10"
}
```

### Response
```json
{
  "id": 1,
  "notes": null,
  "type": "RECEIVER",
  "organ_type": "LIVER",
  "start_date": "2020-02-10",
  "end_date": null,
  "person": {
    "id": 1,
    "created_at": "2022-12-08 15:26:31.731578",
    "updated_at": null,
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "abo": "A",
    "rhesus": "Rhesus.POSITIVE",
    "user": null
  },
  "organ": {
    "id": 1,
    "tumors_count": 2,
    "biggest_tumor_size": 10,
    "alpha_fetoprotein": 10,
    "listing_id": 1
  },
  "hospital": null
}
```

**Status:** 200

## POST /api/listings/1
Update only a subset of the fields of a listing

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "organ": {
    "alpha_fetoprotein": 20
  },
  "person": {
    "first_name": "Jojo"
  }
}
```

### Response
```json
{
  "id": 1,
  "notes": null,
  "type": "RECEIVER",
  "organ_type": "LIVER",
  "start_date": "2020-02-10",
  "end_date": null,
  "person": {
    "id": 1,
    "created_at": "2022-12-08 15:26:31.731578",
    "updated_at": "2022-12-08 15:26:31.925443",
    "first_name": "Jojo",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "abo": "A",
    "rhesus": "Rhesus.POSITIVE",
    "user": null
  },
  "organ": {
    "id": 1,
    "tumors_count": 2,
    "biggest_tumor_size": 10,
    "alpha_fetoprotein": 20,
    "listing_id": 1
  },
  "hospital": null
}
```

**Status:** 200

## GET /api/listings/
Get all listings

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "id": 1,
    "notes": null,
    "type": "RECEIVER",
    "organ_type": "LIVER",
    "start_date": "2020-02-10",
    "end_date": null,
    "person": {
      "id": 1,
      "created_at": "2022-12-08 15:26:31.731578",
      "updated_at": "2022-12-08 15:26:31.925443",
      "first_name": "Jojo",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": {
      "id": 1,
      "tumors_count": 2,
      "biggest_tumor_size": 10,
      "alpha_fetoprotein": 20,
      "listing_id": 1
    },
    "hospital": null
  },
  {
    "id": 2,
    "notes": null,
    "type": "RECEIVER",
    "organ_type": "LUNG",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 2,
      "created_at": "2022-12-08 15:26:31.759343",
      "updated_at": null,
      "first_name": "John",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": {
      "id": 1,
      "diagnosis_group": "A",
      "detailed_diagnosis": "LAM",
      "body_mass_index": 17.9,
      "diabetes": false,
      "assistance_required": false,
      "pulmonary_function_percentage": 0.85,
      "pulmonary_artery_systolic": 25.2,
      "oxygen_requirement": 0.5,
      "six_minutes_walk_distance_over_150_feet": true,
      "continuous_mech_ventilation": true,
      "carbon_dioxide_partial_pressure": 36.3,
      "carbon_dioxide_partial_pressure_15_percent_increase": false,
      "creatinine": 10.2,
      "activities_of_daily_life_required": false,
      "pulmonary_capilary_wedge_pressure": 9.2,
      "listing_id": 2
    },
    "hospital": null
  },
  {
    "id": 3,
    "notes": null,
    "type": "RECEIVER",
    "organ_type": "KIDNEY",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 3,
      "created_at": "2022-12-08 15:26:31.788394",
      "updated_at": null,
      "first_name": "John",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": {
      "id": 1,
      "is_under_dialysis": true,
      "is_retransplantation": false,
      "dialysis_start_date": "2022-12-12",
      "dialysis_end_date": null,
      "arf_date": "2022-12-12",
      "date_transplantation": "2022-12-12",
      "re_registration_date": "2022-12-12",
      "A": 1.2,
      "B": 1.3,
      "DR": 1.4,
      "DQ": 1.5,
      "listing_id": 3
    },
    "hospital": null
  },
  {
    "id": 4,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 4,
      "created_at": "2022-12-08 15:26:31.817156",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": null,
    "hospital": null
  },
  {
    "id": 5,
    "notes": null,
    "type": "DONOR",
    "organ_type": "KIDNEY",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 5,
      "created_at": "2022-12-08 15:26:31.842991",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": null,
    "hospital": null
  },
  {
    "id": 6,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LUNG",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 6,
      "created_at": "2022-12-08 15:26:31.878462",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": null,
    "hospital": null
  }
]
```

**Status:** 200

## GET /api/listings/?type=donor
Only get donor listings

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "id": 4,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 4,
      "created_at": "2022-12-08 15:26:31.817156",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": null,
    "hospital": null
  },
  {
    "id": 5,
    "notes": null,
    "type": "DONOR",
    "organ_type": "KIDNEY",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 5,
      "created_at": "2022-12-08 15:26:31.842991",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": null,
    "hospital": null
  },
  {
    "id": 6,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LUNG",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 6,
      "created_at": "2022-12-08 15:26:31.878462",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": null,
    "hospital": null
  }
]
```

**Status:** 200

## GET /api/listings/?type=receiver
Only get receiver listings

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "id": 1,
    "notes": null,
    "type": "RECEIVER",
    "organ_type": "LIVER",
    "start_date": "2020-02-10",
    "end_date": null,
    "person": {
      "id": 1,
      "created_at": "2022-12-08 15:26:31.731578",
      "updated_at": "2022-12-08 15:26:31.925443",
      "first_name": "Jojo",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": {
      "id": 1,
      "tumors_count": 2,
      "biggest_tumor_size": 10,
      "alpha_fetoprotein": 20,
      "listing_id": 1
    },
    "hospital": null
  },
  {
    "id": 2,
    "notes": null,
    "type": "RECEIVER",
    "organ_type": "LUNG",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 2,
      "created_at": "2022-12-08 15:26:31.759343",
      "updated_at": null,
      "first_name": "John",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": {
      "id": 1,
      "diagnosis_group": "A",
      "detailed_diagnosis": "LAM",
      "body_mass_index": 17.9,
      "diabetes": false,
      "assistance_required": false,
      "pulmonary_function_percentage": 0.85,
      "pulmonary_artery_systolic": 25.2,
      "oxygen_requirement": 0.5,
      "six_minutes_walk_distance_over_150_feet": true,
      "continuous_mech_ventilation": true,
      "carbon_dioxide_partial_pressure": 36.3,
      "carbon_dioxide_partial_pressure_15_percent_increase": false,
      "creatinine": 10.2,
      "activities_of_daily_life_required": false,
      "pulmonary_capilary_wedge_pressure": 9.2,
      "listing_id": 2
    },
    "hospital": null
  },
  {
    "id": 3,
    "notes": null,
    "type": "RECEIVER",
    "organ_type": "KIDNEY",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 3,
      "created_at": "2022-12-08 15:26:31.788394",
      "updated_at": null,
      "first_name": "John",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": {
      "id": 1,
      "is_under_dialysis": true,
      "is_retransplantation": false,
      "dialysis_start_date": "2022-12-12",
      "dialysis_end_date": null,
      "arf_date": "2022-12-12",
      "date_transplantation": "2022-12-12",
      "re_registration_date": "2022-12-12",
      "A": 1.2,
      "B": 1.3,
      "DR": 1.4,
      "DQ": 1.5,
      "listing_id": 3
    },
    "hospital": null
  }
]
```

**Status:** 200

## GET /api/listings/1
Get a specific listing

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "id": 1,
  "notes": null,
  "type": "RECEIVER",
  "organ_type": "LIVER",
  "start_date": "2020-02-10",
  "end_date": null,
  "person": {
    "id": 1,
    "created_at": "2022-12-08 15:26:31.731578",
    "updated_at": "2022-12-08 15:26:31.925443",
    "first_name": "Jojo",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "abo": "A",
    "rhesus": "Rhesus.POSITIVE",
    "user": null
  },
  "organ": {
    "id": 1,
    "tumors_count": 2,
    "biggest_tumor_size": 10,
    "alpha_fetoprotein": 20,
    "listing_id": 1
  },
  "hospital": null
}
```

**Status:** 200

## GET /api/listings/4/matches
Get a list of all matching receivers for a liver listing, with the score

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "donor": {
    "id": 4,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 4,
      "created_at": "2022-12-08 15:26:31.817156",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": null,
    "hospital": null
  },
  "matches": [
    {
      "receiver": {
        "id": 1,
        "notes": null,
        "type": "RECEIVER",
        "organ_type": "LIVER",
        "start_date": "2020-02-10",
        "end_date": null,
        "person": {
          "id": 1,
          "created_at": "2022-12-08 15:26:31.731578",
          "updated_at": "2022-12-08 15:26:31.925443",
          "first_name": "Jojo",
          "last_name": "Doe",
          "birth_date": "1990-02-10",
          "description": null,
          "gender": "MALE",
          "abo": "A",
          "rhesus": "Rhesus.POSITIVE",
          "user": null
        },
        "organ": {
          "id": 1,
          "tumors_count": 2,
          "biggest_tumor_size": 10,
          "alpha_fetoprotein": 20,
          "listing_id": 1
        },
        "hospital": null
      },
      "score": 0.07384824470182078
    }
  ]
}
```

**Status:** 200

## GET /api/listings/5/matches
Get a list of all matching receivers for a lung listing, with the score

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "donor": {
    "id": 5,
    "notes": null,
    "type": "DONOR",
    "organ_type": "KIDNEY",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 5,
      "created_at": "2022-12-08 15:26:31.842991",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": null,
    "hospital": null
  },
  "matches": [
    {
      "receiver": {
        "id": 3,
        "notes": null,
        "type": "RECEIVER",
        "organ_type": "KIDNEY",
        "start_date": null,
        "end_date": null,
        "person": {
          "id": 3,
          "created_at": "2022-12-08 15:26:31.788394",
          "updated_at": null,
          "first_name": "John",
          "last_name": "Doe",
          "birth_date": "1990-02-10",
          "description": null,
          "gender": "MALE",
          "abo": "A",
          "rhesus": "Rhesus.POSITIVE",
          "user": null
        },
        "organ": {
          "id": 1,
          "is_under_dialysis": true,
          "is_retransplantation": false,
          "dialysis_start_date": "2022-12-12",
          "dialysis_end_date": null,
          "arf_date": "2022-12-12",
          "date_transplantation": "2022-12-12",
          "re_registration_date": "2022-12-12",
          "A": 1.2,
          "B": 1.3,
          "DR": 1.4,
          "DQ": 1.5,
          "listing_id": 3
        },
        "hospital": null
      },
      "score": 116339.7268385715
    }
  ]
}
```

**Status:** 200

## GET /api/listings/6/matches
Get a list of all matching receivers for a kidney listing, with the score

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "donor": {
    "id": 6,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LUNG",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 6,
      "created_at": "2022-12-08 15:26:31.878462",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "abo": "A",
      "rhesus": "Rhesus.POSITIVE",
      "user": null
    },
    "organ": null,
    "hospital": null
  },
  "matches": [
    {
      "receiver": {
        "id": 2,
        "notes": null,
        "type": "RECEIVER",
        "organ_type": "LUNG",
        "start_date": null,
        "end_date": null,
        "person": {
          "id": 2,
          "created_at": "2022-12-08 15:26:31.759343",
          "updated_at": null,
          "first_name": "John",
          "last_name": "Doe",
          "birth_date": "1990-02-10",
          "description": null,
          "gender": "MALE",
          "abo": "A",
          "rhesus": "Rhesus.POSITIVE",
          "user": null
        },
        "organ": {
          "id": 1,
          "diagnosis_group": "A",
          "detailed_diagnosis": "LAM",
          "body_mass_index": 17.9,
          "diabetes": false,
          "assistance_required": false,
          "pulmonary_function_percentage": 0.85,
          "pulmonary_artery_systolic": 25.2,
          "oxygen_requirement": 0.5,
          "six_minutes_walk_distance_over_150_feet": true,
          "continuous_mech_ventilation": true,
          "carbon_dioxide_partial_pressure": 36.3,
          "carbon_dioxide_partial_pressure_15_percent_increase": false,
          "creatinine": 10.2,
          "activities_of_daily_life_required": false,
          "pulmonary_capilary_wedge_pressure": 9.2,
          "listing_id": 2
        },
        "hospital": null
      },
      "score": "-58472.76922253629706797450640"
    }
  ]
}
```

**Status:** 200

## DELETE /api/listings/2
Delete a listing

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 204

