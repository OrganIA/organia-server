# API Documentation
Generated on: 2022-12-05 at 00:45:51

- [GET /api/](#get--api-)
- [POST /api/auth/register](#post--api-auth-register)
- [POST /api/auth/login](#post--api-auth-login)
- [GET /api/users](#get--api-users)
- [GET /api/users/me](#get--api-users-me)
- [GET /api/users/1](#get--api-users-1)
- [DELETE /api/users/3](#delete--api-users-3)
- [GET /api/listings](#get--api-listings)
- [GET /api/listings/1](#get--api-listings-1)
- [GET /api/listings/1/matches](#get--api-listings-1-matches)
- [GET /api/listings/?type=donor](#get--api-listings-?type=donor)
- [GET /api/listings/?type=receiver](#get--api-listings-?type=receiver)
- [POST /api/chats](#post--api-chats)
- [GET /api/chats](#get--api-chats)
- [GET /api/chats/1](#get--api-chats-1)
- [POST /api/chats/1/messages](#post--api-chats-1-messages)
- [GET /api/chats/messages/latest](#get--api-chats-messages-latest)
- [GET /api/chats/1/messages](#get--api-chats-1-messages)
- [DELETE /api/chats/1](#delete--api-chats-1)
- [GET /api/roles](#get--api-roles)
- [GET /api/roles/1](#get--api-roles-1)
- [POST /api/roles](#post--api-roles)
- [POST /api/roles/3](#post--api-roles-3)
- [DELETE /api/roles/3](#delete--api-roles-3)


## GET /api/
Information about the server, such as the version or the OS.
Useful to check if the server is up, or to check if it is running
the latest version.

### Response
```json
{
  "version": "9df8949",
  "time": 1670193951.837005,
  "datetime": "2022-12-04 23:45:51.837005",
  "software": {
    "flask": "2.2.2",
    "python": "3.10.8",
    "system": {
      "name": "Arch Linux",
      "platform": "Linux",
      "release": "6.0.11-arch1-1",
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
  "email": "user787@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "token": "4-4-76189e90d50eca18710208115fafbe75224228544d7d36e773dae181233c96e1",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 4,
    "created_at": "2022-12-04 23:45:52.046803",
    "updated_at": null,
    "email": "user787@email.com",
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
  "email": "user787@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "msg": "email \"user787@email.com\" is already taken."
}
```

**Status:** 422

## POST /api/auth/login
Login and get a token.

### Request
```json
{
  "email": "user787@email.com",
  "password": "password"
}
```

### Response
```json
{
  "token": "5-4-9aa27adda0fa45e7d09a157daffd03e9ae91562f1107b96940d89afa4781d4d0",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 4,
    "created_at": "2022-12-04 23:45:52.046803",
    "updated_at": null,
    "email": "user787@email.com",
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
  "email": "user787@email.com",
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
    "created_at": "2022-12-04 23:34:15.038647",
    "updated_at": null,
    "email": "user932@email.com",
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
    "created_at": "2022-12-04 23:34:15.452561",
    "updated_at": null,
    "email": "user130@email.com",
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
    "created_at": "2022-12-04 23:34:16.100503",
    "updated_at": "2022-12-04 23:34:16.116027",
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
  {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 4,
    "created_at": "2022-12-04 23:45:52.046803",
    "updated_at": null,
    "email": "user787@email.com",
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
  "created_at": "2022-12-04 23:34:16.100503",
  "updated_at": "2022-12-04 23:34:16.116027",
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
  "created_at": "2022-12-04 23:34:15.038647",
  "updated_at": null,
  "email": "user932@email.com",
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

## GET /api/listings
Get the list of listings

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "id": 1,
    "notes": "note",
    "type": "DONOR",
    "organ": "HEART",
    "tumors_number": 0,
    "biggest_tumor_size": null,
    "alpha_fetoprotein": null,
    "is_under_dialysis": null,
    "dialysis_start_date": null,
    "dialysis_end_date": null,
    "is_retransplantation": null,
    "arf_date": null,
    "transplantation_date": null,
    "re_registration_date": null,
    "A": null,
    "B": null,
    "DR": null,
    "DQ": null,
    "hospital_id": null,
    "person": null
  },
  {
    "id": 2,
    "notes": "note",
    "type": "RECEIVER",
    "organ": "HEART",
    "tumors_number": 0,
    "biggest_tumor_size": null,
    "alpha_fetoprotein": null,
    "is_under_dialysis": null,
    "dialysis_start_date": null,
    "dialysis_end_date": null,
    "is_retransplantation": null,
    "arf_date": null,
    "transplantation_date": null,
    "re_registration_date": null,
    "A": null,
    "B": null,
    "DR": null,
    "DQ": null,
    "hospital_id": null,
    "person": null
  }
]
```

**Status:** 200
### Request
```json
{
  "page": 2,
  "per_page": 10
}
```

### Response
```json
[
  {
    "id": 1,
    "notes": "note",
    "type": "DONOR",
    "organ": "HEART",
    "tumors_number": 0,
    "biggest_tumor_size": null,
    "alpha_fetoprotein": null,
    "is_under_dialysis": null,
    "dialysis_start_date": null,
    "dialysis_end_date": null,
    "is_retransplantation": null,
    "arf_date": null,
    "transplantation_date": null,
    "re_registration_date": null,
    "A": null,
    "B": null,
    "DR": null,
    "DQ": null,
    "hospital_id": null,
    "person": null
  },
  {
    "id": 2,
    "notes": "note",
    "type": "RECEIVER",
    "organ": "HEART",
    "tumors_number": 0,
    "biggest_tumor_size": null,
    "alpha_fetoprotein": null,
    "is_under_dialysis": null,
    "dialysis_start_date": null,
    "dialysis_end_date": null,
    "is_retransplantation": null,
    "arf_date": null,
    "transplantation_date": null,
    "re_registration_date": null,
    "A": null,
    "B": null,
    "DR": null,
    "DQ": null,
    "hospital_id": null,
    "person": null
  }
]
```

**Status:** 200
### Request
```json
{
  "search": "jean"
}
```

### Response
```json
[
  {
    "id": 1,
    "notes": "note",
    "type": "DONOR",
    "organ": "HEART",
    "tumors_number": 0,
    "biggest_tumor_size": null,
    "alpha_fetoprotein": null,
    "is_under_dialysis": null,
    "dialysis_start_date": null,
    "dialysis_end_date": null,
    "is_retransplantation": null,
    "arf_date": null,
    "transplantation_date": null,
    "re_registration_date": null,
    "A": null,
    "B": null,
    "DR": null,
    "DQ": null,
    "hospital_id": null,
    "person": null
  },
  {
    "id": 2,
    "notes": "note",
    "type": "RECEIVER",
    "organ": "HEART",
    "tumors_number": 0,
    "biggest_tumor_size": null,
    "alpha_fetoprotein": null,
    "is_under_dialysis": null,
    "dialysis_start_date": null,
    "dialysis_end_date": null,
    "is_retransplantation": null,
    "arf_date": null,
    "transplantation_date": null,
    "re_registration_date": null,
    "A": null,
    "B": null,
    "DR": null,
    "DQ": null,
    "hospital_id": null,
    "person": null
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
  "notes": "note",
  "type": "DONOR",
  "organ": "HEART",
  "tumors_number": 0,
  "biggest_tumor_size": null,
  "alpha_fetoprotein": null,
  "is_under_dialysis": null,
  "dialysis_start_date": null,
  "dialysis_end_date": null,
  "is_retransplantation": null,
  "arf_date": null,
  "transplantation_date": null,
  "re_registration_date": null,
  "A": null,
  "B": null,
  "DR": null,
  "DQ": null,
  "hospital_id": null,
  "person": null
}
```

**Status:** 200

## GET /api/listings/1/matches
Get the matching listings for an organ

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

**Status:** 500

## GET /api/listings/?type=donor
Only get donor listings

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "id": 1,
    "notes": "note",
    "type": "DONOR",
    "organ": "HEART",
    "tumors_number": 0,
    "biggest_tumor_size": null,
    "alpha_fetoprotein": null,
    "is_under_dialysis": null,
    "dialysis_start_date": null,
    "dialysis_end_date": null,
    "is_retransplantation": null,
    "arf_date": null,
    "transplantation_date": null,
    "re_registration_date": null,
    "A": null,
    "B": null,
    "DR": null,
    "DQ": null,
    "hospital_id": null,
    "person": null
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
    "id": 2,
    "notes": "note",
    "type": "RECEIVER",
    "organ": "HEART",
    "tumors_number": 0,
    "biggest_tumor_size": null,
    "alpha_fetoprotein": null,
    "is_under_dialysis": null,
    "dialysis_start_date": null,
    "dialysis_end_date": null,
    "is_retransplantation": null,
    "arf_date": null,
    "transplantation_date": null,
    "re_registration_date": null,
    "A": null,
    "B": null,
    "DR": null,
    "DQ": null,
    "hospital_id": null,
    "person": null
  }
]
```

**Status:** 200

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
  "created_at": "2022-12-04 23:45:52.895684",
  "updated_at": null,
  "name": "Chat name",
  "users": [
    {
      "firstname": "prenom",
      "lastname": "nom",
      "id": 1,
      "created_at": "2022-12-04 23:34:15.038647",
      "updated_at": null,
      "email": "user932@email.com",
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
      "created_at": "2022-12-04 23:34:15.452561",
      "updated_at": null,
      "email": "user130@email.com",
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
      "id": 5,
      "created_at": "2022-12-04 23:45:52.761502",
      "updated_at": "2022-12-04 23:45:52.775655",
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
    "id": 5,
    "created_at": "2022-12-04 23:45:52.761502",
    "updated_at": "2022-12-04 23:45:52.775655",
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
    "created_at": "2022-12-04 23:45:52.895684",
    "updated_at": null,
    "name": "Chat name",
    "users": [
      {
        "firstname": "prenom",
        "lastname": "nom",
        "id": 1,
        "created_at": "2022-12-04 23:34:15.038647",
        "updated_at": null,
        "email": "user932@email.com",
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
        "created_at": "2022-12-04 23:34:15.452561",
        "updated_at": null,
        "email": "user130@email.com",
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
        "id": 5,
        "created_at": "2022-12-04 23:45:52.761502",
        "updated_at": "2022-12-04 23:45:52.775655",
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
      "id": 5,
      "created_at": "2022-12-04 23:45:52.761502",
      "updated_at": "2022-12-04 23:45:52.775655",
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
  "created_at": "2022-12-04 23:45:52.895684",
  "updated_at": null,
  "name": "Chat name",
  "users": [
    {
      "firstname": "prenom",
      "lastname": "nom",
      "id": 1,
      "created_at": "2022-12-04 23:34:15.038647",
      "updated_at": null,
      "email": "user932@email.com",
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
      "created_at": "2022-12-04 23:34:15.452561",
      "updated_at": null,
      "email": "user130@email.com",
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
      "id": 5,
      "created_at": "2022-12-04 23:45:52.761502",
      "updated_at": "2022-12-04 23:45:52.775655",
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
    "id": 5,
    "created_at": "2022-12-04 23:45:52.761502",
    "updated_at": "2022-12-04 23:45:52.775655",
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
    "created_at": "2022-12-04 23:45:52.895684",
    "updated_at": null,
    "name": "Chat name",
    "users": [
      {
        "firstname": "prenom",
        "lastname": "nom",
        "id": 1,
        "created_at": "2022-12-04 23:34:15.038647",
        "updated_at": null,
        "email": "user932@email.com",
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
        "created_at": "2022-12-04 23:34:15.452561",
        "updated_at": null,
        "email": "user130@email.com",
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
        "id": 5,
        "created_at": "2022-12-04 23:45:52.761502",
        "updated_at": "2022-12-04 23:45:52.775655",
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
      "id": 5,
      "created_at": "2022-12-04 23:45:52.761502",
      "updated_at": "2022-12-04 23:45:52.775655",
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
    "id": 5,
    "created_at": "2022-12-04 23:45:52.761502",
    "updated_at": "2022-12-04 23:45:52.775655",
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
  "id": 2
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
    "chat": {
      "id": 1,
      "created_at": "2022-12-04 23:45:52.895684",
      "updated_at": null,
      "name": "Chat name",
      "users": [
        {
          "firstname": "prenom",
          "lastname": "nom",
          "id": 1,
          "created_at": "2022-12-04 23:34:15.038647",
          "updated_at": null,
          "email": "user932@email.com",
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
          "created_at": "2022-12-04 23:34:15.452561",
          "updated_at": null,
          "email": "user130@email.com",
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
          "id": 5,
          "created_at": "2022-12-04 23:45:52.761502",
          "updated_at": "2022-12-04 23:45:52.775655",
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
        "id": 5,
        "created_at": "2022-12-04 23:45:52.761502",
        "updated_at": "2022-12-04 23:45:52.775655",
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
    "last_message": {
      "content": "Hello world!",
      "chat": {
        "id": 1,
        "created_at": "2022-12-04 23:45:52.895684",
        "updated_at": null,
        "name": "Chat name",
        "users": [
          {
            "firstname": "prenom",
            "lastname": "nom",
            "id": 1,
            "created_at": "2022-12-04 23:34:15.038647",
            "updated_at": null,
            "email": "user932@email.com",
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
            "created_at": "2022-12-04 23:34:15.452561",
            "updated_at": null,
            "email": "user130@email.com",
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
            "id": 5,
            "created_at": "2022-12-04 23:45:52.761502",
            "updated_at": "2022-12-04 23:45:52.775655",
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
          "id": 5,
          "created_at": "2022-12-04 23:45:52.761502",
          "updated_at": "2022-12-04 23:45:52.775655",
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
        "id": 5,
        "created_at": "2022-12-04 23:45:52.761502",
        "updated_at": "2022-12-04 23:45:52.775655",
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
      "id": 2
    }
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
      "created_at": "2022-12-04 23:45:52.895684",
      "updated_at": null,
      "name": "Chat name",
      "users": [
        {
          "firstname": "prenom",
          "lastname": "nom",
          "id": 1,
          "created_at": "2022-12-04 23:34:15.038647",
          "updated_at": null,
          "email": "user932@email.com",
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
          "created_at": "2022-12-04 23:34:15.452561",
          "updated_at": null,
          "email": "user130@email.com",
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
          "id": 5,
          "created_at": "2022-12-04 23:45:52.761502",
          "updated_at": "2022-12-04 23:45:52.775655",
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
        "id": 5,
        "created_at": "2022-12-04 23:45:52.761502",
        "updated_at": "2022-12-04 23:45:52.775655",
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
      "id": 5,
      "created_at": "2022-12-04 23:45:52.761502",
      "updated_at": "2022-12-04 23:45:52.775655",
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
    "id": 2
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

