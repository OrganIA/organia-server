# API Documentation
Generated on: 2022-12-07 at 23:48:59

- [GET /api/](#get-api)
- [POST /api/auth/register](#post-apiauthregister)
- [POST /api/auth/login](#post-apiauthlogin)
- [GET /api/users](#get-apiusers)
- [GET /api/users/me](#get-apiusersme)
- [GET /api/users/1](#get-apiusers1)
- [DELETE /api/users/3](#delete-apiusers3)
- [GET /api/listings](#get-apilistings)
- [GET /api/listings/1](#get-apilistings1)
- [GET /api/listings/1/matches](#get-apilistings1matches)
- [GET /api/listings/?type=donor](#get-apilistingstypedonor)
- [GET /api/listings/?type=receiver](#get-apilistingstypereceiver)
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


## GET /api/
Information about the server, such as the version or the OS.
Useful to check if the server is up, or to check if it is running
the latest version.

### Response
```json
{
  "version": "80297ea",
  "time": 1670449739.31508,
  "datetime": "2022-12-07 22:48:59.315080",
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
  "email": "user541@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "token": "4-4-ef93fa52b8be051a37c660332160da5d0702624bdab414af5fb6703ee7c9b94a",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 4,
    "created_at": "2022-12-07 22:48:59.531835",
    "updated_at": null,
    "email": "user541@email.com",
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
  "email": "user541@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "msg": "email \"user541@email.com\" is already taken."
}
```

**Status:** 422

## POST /api/auth/login
Login and get a token.

### Request
```json
{
  "email": "user541@email.com",
  "password": "password"
}
```

### Response
```json
{
  "token": "6-4-11eb95d4ea84d1b92ff65306ae54ea6d4a5e9f33c49a954de2dc2e24ae9c8bed",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 4,
    "created_at": "2022-12-07 22:48:59.531835",
    "updated_at": null,
    "email": "user541@email.com",
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
  "email": "user541@email.com",
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
    "created_at": "2022-12-07 22:42:57.245972",
    "updated_at": null,
    "email": "user799@email.com",
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
    "created_at": "2022-12-07 22:42:57.613819",
    "updated_at": null,
    "email": "user601@email.com",
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
    "created_at": "2022-12-07 22:42:58.254591",
    "updated_at": "2022-12-07 22:42:58.263127",
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
    "created_at": "2022-12-07 22:48:59.531835",
    "updated_at": null,
    "email": "user541@email.com",
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
    "id": 5,
    "created_at": "2022-12-07 22:48:59.894886",
    "updated_at": null,
    "email": "user38@email.com",
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
  "created_at": "2022-12-07 22:42:58.254591",
  "updated_at": "2022-12-07 22:42:58.263127",
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
  "created_at": "2022-12-07 22:42:57.245972",
  "updated_at": null,
  "email": "user799@email.com",
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
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 1,
      "created_at": "2022-12-07 22:42:58.525043",
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
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 1,
      "created_at": "2022-12-07 22:42:58.525043",
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
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 1,
      "created_at": "2022-12-07 22:42:58.525043",
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
  "type": "DONOR",
  "organ_type": "LIVER",
  "start_date": null,
  "end_date": null,
  "person": {
    "id": 1,
    "created_at": "2022-12-07 22:42:58.525043",
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

## GET /api/listings/1/matches
Get the matching listings for an organ

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "donor": {
    "id": 1,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 1,
      "created_at": "2022-12-07 22:42:58.525043",
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
  },
  "matches": []
}
```

**Status:** 200

## GET /api/listings/?type=donor
Only get donor listings

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "id": 1,
    "notes": null,
    "type": "DONOR",
    "organ_type": "LIVER",
    "start_date": null,
    "end_date": null,
    "person": {
      "id": 1,
      "created_at": "2022-12-07 22:42:58.525043",
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
]
```

**Status:** 200

## GET /api/listings/?type=receiver
Only get receiver listings

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[]
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
  "created_at": "2022-12-07 22:49:00.579924",
  "updated_at": null,
  "name": "Chat name",
  "users": [
    {
      "firstname": "prenom",
      "lastname": "nom",
      "id": 1,
      "created_at": "2022-12-07 22:42:57.245972",
      "updated_at": null,
      "email": "user799@email.com",
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
      "created_at": "2022-12-07 22:42:57.613819",
      "updated_at": null,
      "email": "user601@email.com",
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
      "id": 6,
      "created_at": "2022-12-07 22:49:00.481058",
      "updated_at": "2022-12-07 22:49:00.488647",
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
    "id": 6,
    "created_at": "2022-12-07 22:49:00.481058",
    "updated_at": "2022-12-07 22:49:00.488647",
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
    "created_at": "2022-12-07 22:49:00.579924",
    "updated_at": null,
    "name": "Chat name",
    "users": [
      {
        "firstname": "prenom",
        "lastname": "nom",
        "id": 1,
        "created_at": "2022-12-07 22:42:57.245972",
        "updated_at": null,
        "email": "user799@email.com",
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
        "created_at": "2022-12-07 22:42:57.613819",
        "updated_at": null,
        "email": "user601@email.com",
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
        "id": 6,
        "created_at": "2022-12-07 22:49:00.481058",
        "updated_at": "2022-12-07 22:49:00.488647",
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
      "id": 6,
      "created_at": "2022-12-07 22:49:00.481058",
      "updated_at": "2022-12-07 22:49:00.488647",
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
  "created_at": "2022-12-07 22:49:00.579924",
  "updated_at": null,
  "name": "Chat name",
  "users": [
    {
      "firstname": "prenom",
      "lastname": "nom",
      "id": 1,
      "created_at": "2022-12-07 22:42:57.245972",
      "updated_at": null,
      "email": "user799@email.com",
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
      "created_at": "2022-12-07 22:42:57.613819",
      "updated_at": null,
      "email": "user601@email.com",
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
      "id": 6,
      "created_at": "2022-12-07 22:49:00.481058",
      "updated_at": "2022-12-07 22:49:00.488647",
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
    "id": 6,
    "created_at": "2022-12-07 22:49:00.481058",
    "updated_at": "2022-12-07 22:49:00.488647",
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
    "created_at": "2022-12-07 22:49:00.579924",
    "updated_at": null,
    "name": "Chat name",
    "users": [
      {
        "firstname": "prenom",
        "lastname": "nom",
        "id": 1,
        "created_at": "2022-12-07 22:42:57.245972",
        "updated_at": null,
        "email": "user799@email.com",
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
        "created_at": "2022-12-07 22:42:57.613819",
        "updated_at": null,
        "email": "user601@email.com",
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
        "id": 6,
        "created_at": "2022-12-07 22:49:00.481058",
        "updated_at": "2022-12-07 22:49:00.488647",
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
      "id": 6,
      "created_at": "2022-12-07 22:49:00.481058",
      "updated_at": "2022-12-07 22:49:00.488647",
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
    "id": 6,
    "created_at": "2022-12-07 22:49:00.481058",
    "updated_at": "2022-12-07 22:49:00.488647",
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
  "id": 2,
  "created_at": "2022-12-07 22:49:00.634940"
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
      "created_at": "2022-12-07 22:49:00.579924",
      "updated_at": null,
      "name": "Chat name",
      "users": [
        {
          "firstname": "prenom",
          "lastname": "nom",
          "id": 1,
          "created_at": "2022-12-07 22:42:57.245972",
          "updated_at": null,
          "email": "user799@email.com",
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
          "created_at": "2022-12-07 22:42:57.613819",
          "updated_at": null,
          "email": "user601@email.com",
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
          "id": 6,
          "created_at": "2022-12-07 22:49:00.481058",
          "updated_at": "2022-12-07 22:49:00.488647",
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
        "id": 6,
        "created_at": "2022-12-07 22:49:00.481058",
        "updated_at": "2022-12-07 22:49:00.488647",
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
      "id": 6,
      "created_at": "2022-12-07 22:49:00.481058",
      "updated_at": "2022-12-07 22:49:00.488647",
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
    "id": 2,
    "created_at": "2022-12-07 22:49:00.634940"
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
      "created_at": "2022-12-07 22:49:00.579924",
      "updated_at": null,
      "name": "Chat name",
      "users": [
        {
          "firstname": "prenom",
          "lastname": "nom",
          "id": 1,
          "created_at": "2022-12-07 22:42:57.245972",
          "updated_at": null,
          "email": "user799@email.com",
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
          "created_at": "2022-12-07 22:42:57.613819",
          "updated_at": null,
          "email": "user601@email.com",
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
          "id": 6,
          "created_at": "2022-12-07 22:49:00.481058",
          "updated_at": "2022-12-07 22:49:00.488647",
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
        "id": 6,
        "created_at": "2022-12-07 22:49:00.481058",
        "updated_at": "2022-12-07 22:49:00.488647",
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
      "id": 6,
      "created_at": "2022-12-07 22:49:00.481058",
      "updated_at": "2022-12-07 22:49:00.488647",
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
    "id": 2,
    "created_at": "2022-12-07 22:49:00.634940"
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
Create a listing, creating the Person and Organ in one go

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "type": "DONOR",
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
  "id": 2,
  "notes": null,
  "type": "DONOR",
  "organ_type": "LIVER",
  "start_date": null,
  "end_date": null,
  "person": {
    "id": 2,
    "created_at": "2022-12-07 22:49:00.797416",
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
    "id": 2,
    "tumors_count": 2,
    "biggest_tumor_size": 10,
    "alpha_fetoprotein": 10,
    "listing_id": 2
  },
  "hospital": null
}
```

**Status:** 200

