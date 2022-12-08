# API Documentation
Generated on: 2022-12-08 at 03:24:15

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
- [POST /api/listings/1](#post-apilistings1)
- [POST /api/listings/1](#post-apilistings1)
- [GET /api/listings/](#get-apilistings)
- [GET /api/listings/?type=donor](#get-apilistingstypedonor)
- [GET /api/listings/?type=receiver](#get-apilistingstypereceiver)
- [GET /api/listings/1](#get-apilistings1)
- [GET /api/listings/2/matches](#get-apilistings2matches)
- [DELETE /api/listings/1](#delete-apilistings1)


## GET /api/
Information about the server, such as the version or the OS.
Useful to check if the server is up, or to check if it is running
the latest version.

### Response
```json
{
  "version": "dfd1928",
  "time": 1670462655.19432,
  "datetime": "2022-12-08 02:24:15.194320",
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
  "email": "user773@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "token": "1-1-e0a444bd391f7be1cbec22e1e1f017619799c4b1cd8bfad4680898c3e389548d",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 1,
    "created_at": "2022-12-08 02:24:15.406039",
    "updated_at": null,
    "email": "user773@email.com",
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
  "email": "user773@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "msg": "email \"user773@email.com\" is already taken."
}
```

**Status:** 422

## POST /api/auth/login
Login and get a token.

### Request
```json
{
  "email": "user773@email.com",
  "password": "password"
}
```

### Response
```json
{
  "token": "3-1-3853090eb0686349c06b1e083361596ad1fdddbd86bec1288ba2dd7b4fa0140a",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 1,
    "created_at": "2022-12-08 02:24:15.406039",
    "updated_at": null,
    "email": "user773@email.com",
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
  "email": "user773@email.com",
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
    "created_at": "2022-12-08 02:24:15.406039",
    "updated_at": null,
    "email": "user773@email.com",
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
    "created_at": "2022-12-08 02:24:15.754427",
    "updated_at": null,
    "email": "user746@email.com",
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
    "created_at": "2022-12-08 02:24:16.290573",
    "updated_at": "2022-12-08 02:24:16.300243",
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
  "created_at": "2022-12-08 02:24:16.290573",
  "updated_at": "2022-12-08 02:24:16.300243",
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
  "created_at": "2022-12-08 02:24:15.406039",
  "updated_at": null,
  "email": "user773@email.com",
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
  "created_at": "2022-12-08 02:24:16.387216",
  "updated_at": null,
  "name": "Chat name",
  "users": [
    {
      "firstname": "prenom",
      "lastname": "nom",
      "id": 1,
      "created_at": "2022-12-08 02:24:15.406039",
      "updated_at": null,
      "email": "user773@email.com",
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
      "created_at": "2022-12-08 02:24:15.754427",
      "updated_at": null,
      "email": "user746@email.com",
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
      "created_at": "2022-12-08 02:24:16.369462",
      "updated_at": "2022-12-08 02:24:16.377141",
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
    "created_at": "2022-12-08 02:24:16.369462",
    "updated_at": "2022-12-08 02:24:16.377141",
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
    "created_at": "2022-12-08 02:24:16.387216",
    "updated_at": null,
    "name": "Chat name",
    "users": [
      {
        "firstname": "prenom",
        "lastname": "nom",
        "id": 1,
        "created_at": "2022-12-08 02:24:15.406039",
        "updated_at": null,
        "email": "user773@email.com",
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
        "created_at": "2022-12-08 02:24:15.754427",
        "updated_at": null,
        "email": "user746@email.com",
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
        "created_at": "2022-12-08 02:24:16.369462",
        "updated_at": "2022-12-08 02:24:16.377141",
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
      "created_at": "2022-12-08 02:24:16.369462",
      "updated_at": "2022-12-08 02:24:16.377141",
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
  "created_at": "2022-12-08 02:24:16.387216",
  "updated_at": null,
  "name": "Chat name",
  "users": [
    {
      "firstname": "prenom",
      "lastname": "nom",
      "id": 1,
      "created_at": "2022-12-08 02:24:15.406039",
      "updated_at": null,
      "email": "user773@email.com",
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
      "created_at": "2022-12-08 02:24:15.754427",
      "updated_at": null,
      "email": "user746@email.com",
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
      "created_at": "2022-12-08 02:24:16.369462",
      "updated_at": "2022-12-08 02:24:16.377141",
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
    "created_at": "2022-12-08 02:24:16.369462",
    "updated_at": "2022-12-08 02:24:16.377141",
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
    "created_at": "2022-12-08 02:24:16.387216",
    "updated_at": null,
    "name": "Chat name",
    "users": [
      {
        "firstname": "prenom",
        "lastname": "nom",
        "id": 1,
        "created_at": "2022-12-08 02:24:15.406039",
        "updated_at": null,
        "email": "user773@email.com",
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
        "created_at": "2022-12-08 02:24:15.754427",
        "updated_at": null,
        "email": "user746@email.com",
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
        "created_at": "2022-12-08 02:24:16.369462",
        "updated_at": "2022-12-08 02:24:16.377141",
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
      "created_at": "2022-12-08 02:24:16.369462",
      "updated_at": "2022-12-08 02:24:16.377141",
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
    "created_at": "2022-12-08 02:24:16.369462",
    "updated_at": "2022-12-08 02:24:16.377141",
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
  "created_at": "2022-12-08 02:24:16.439636"
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
      "created_at": "2022-12-08 02:24:16.387216",
      "updated_at": null,
      "name": "Chat name",
      "users": [
        {
          "firstname": "prenom",
          "lastname": "nom",
          "id": 1,
          "created_at": "2022-12-08 02:24:15.406039",
          "updated_at": null,
          "email": "user773@email.com",
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
          "created_at": "2022-12-08 02:24:15.754427",
          "updated_at": null,
          "email": "user746@email.com",
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
          "created_at": "2022-12-08 02:24:16.369462",
          "updated_at": "2022-12-08 02:24:16.377141",
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
        "created_at": "2022-12-08 02:24:16.369462",
        "updated_at": "2022-12-08 02:24:16.377141",
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
      "created_at": "2022-12-08 02:24:16.369462",
      "updated_at": "2022-12-08 02:24:16.377141",
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
    "created_at": "2022-12-08 02:24:16.439636"
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
      "created_at": "2022-12-08 02:24:16.387216",
      "updated_at": null,
      "name": "Chat name",
      "users": [
        {
          "firstname": "prenom",
          "lastname": "nom",
          "id": 1,
          "created_at": "2022-12-08 02:24:15.406039",
          "updated_at": null,
          "email": "user773@email.com",
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
          "created_at": "2022-12-08 02:24:15.754427",
          "updated_at": null,
          "email": "user746@email.com",
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
          "created_at": "2022-12-08 02:24:16.369462",
          "updated_at": "2022-12-08 02:24:16.377141",
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
        "created_at": "2022-12-08 02:24:16.369462",
        "updated_at": "2022-12-08 02:24:16.377141",
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
      "created_at": "2022-12-08 02:24:16.369462",
      "updated_at": "2022-12-08 02:24:16.377141",
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
    "created_at": "2022-12-08 02:24:16.439636"
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
    "created_at": "2022-12-08 02:24:16.599182",
    "updated_at": null,
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "user": null,
    "blood_type": "A+"
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
diagnosis_group can be A, B, C, or D
detailed_diagnosis can be one of the following:
- BRONCHIECTASIS
- EISENMENGER
- BRONCHIOLITIS
- LAM
- SARCOIDOSIS
body_mass_index for a normal person is expected to be between 18.5 and 25
pulmonary_artery_systolic is expected to be between 17 and 20, > 30 is
considered critical
carbon_dioxide_partial_pressure is expected to be between 35 and 40
pulmonary_capilary_wedge_pressure is expected to be between 8 and 12,
> 20 is considered critical

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
    "carbone_dioxide_partial_pressure_15_percent_increase": false,
    "activities_of_daily_life_required": false,
    "pulmonary_capilary_wedge_pressure": 9.2
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
    "created_at": "2022-12-08 02:24:16.625197",
    "updated_at": null,
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "user": null,
    "blood_type": "A+"
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
    "carbone_dioxide_partial_pressure_15_percent_increase": false,
    "creatinine": null,
    "activities_of_daily_life_required": false,
    "pulmonary_capilary_wedge_pressure": 9.2,
    "listing_id": 2
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
  "id": 3,
  "notes": null,
  "type": "DONOR",
  "organ_type": "LIVER",
  "start_date": null,
  "end_date": null,
  "person": {
    "id": 3,
    "created_at": "2022-12-08 02:24:16.652058",
    "updated_at": null,
    "first_name": "Johnatan",
    "last_name": "Joeystarr",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "user": null,
    "blood_type": "A+"
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
    "created_at": "2022-12-08 02:24:16.599182",
    "updated_at": null,
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "user": null,
    "blood_type": "A+"
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
    "created_at": "2022-12-08 02:24:16.599182",
    "updated_at": "2022-12-08 02:24:16.689642",
    "first_name": "Jojo",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "user": null,
    "blood_type": "A+"
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
      "created_at": "2022-12-08 02:24:16.599182",
      "updated_at": "2022-12-08 02:24:16.689642",
      "first_name": "Jojo",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "user": null,
      "blood_type": "A+"
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
      "created_at": "2022-12-08 02:24:16.625197",
      "updated_at": null,
      "first_name": "John",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "user": null,
      "blood_type": "A+"
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
      "carbone_dioxide_partial_pressure_15_percent_increase": false,
      "creatinine": null,
      "activities_of_daily_life_required": false,
      "pulmonary_capilary_wedge_pressure": 9.2,
      "listing_id": 2
    },
    "hospital": null
  },
  {
    "id": 3,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 3,
      "created_at": "2022-12-08 02:24:16.652058",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "user": null,
      "blood_type": "A+"
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
    "id": 3,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 3,
      "created_at": "2022-12-08 02:24:16.652058",
      "updated_at": null,
      "first_name": "Johnatan",
      "last_name": "Joeystarr",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "user": null,
      "blood_type": "A+"
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
      "created_at": "2022-12-08 02:24:16.599182",
      "updated_at": "2022-12-08 02:24:16.689642",
      "first_name": "Jojo",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "user": null,
      "blood_type": "A+"
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
      "created_at": "2022-12-08 02:24:16.625197",
      "updated_at": null,
      "first_name": "John",
      "last_name": "Doe",
      "birth_date": "1990-02-10",
      "description": null,
      "gender": "MALE",
      "user": null,
      "blood_type": "A+"
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
      "carbone_dioxide_partial_pressure_15_percent_increase": false,
      "creatinine": null,
      "activities_of_daily_life_required": false,
      "pulmonary_capilary_wedge_pressure": 9.2,
      "listing_id": 2
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
    "created_at": "2022-12-08 02:24:16.599182",
    "updated_at": "2022-12-08 02:24:16.689642",
    "first_name": "Jojo",
    "last_name": "Doe",
    "birth_date": "1990-02-10",
    "description": null,
    "gender": "MALE",
    "user": null,
    "blood_type": "A+"
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

## GET /api/listings/2/matches
Get a list of all matching receivers for a donor listing, with the score

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "msg": "You can only match from a donor"
}
```

**Status:** 422

## DELETE /api/listings/1
Delete a listing

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 204

