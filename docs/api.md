# API Documentation
Generated on: 2022-11-30 at 01:29:05

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
- [POST /api/chats](#post--api-chats)
- [GET /api/chats](#get--api-chats)
- [GET /api/chats/1](#get--api-chats-1)
- [POST /api/chats/1/messages](#post--api-chats-1-messages)
- [GET /api/chats/messages/latest](#get--api-chats-messages-latest)
- [GET /api/chats/1/messages](#get--api-chats-1-messages)
- [DELETE /api/chats/1](#delete--api-chats-1)


## GET /api/
Information about the server, such as the version or the OS.
Useful to check if the server is up, or to check if it is running
the latest version.

### Response
```json
{
  "version": "69ce359",
  "time": 1669764545.041067,
  "datetime": "2022-11-30 00:29:05.041067",
  "software": {
    "flask": "2.2.2",
    "python": "3.10.6",
    "system": {
      "name": "Arch Linux",
      "platform": "Linux",
      "release": "5.19.5-arch1-1",
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
  "email": "user852@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "token": "7-7-9df8751dad8158ba7dce2fdae61a3e1c057f6b00c37f5078c0fa22ac4d4dfb34",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 7,
    "created_at": "2022-11-30 00:29:05.320363",
    "updated_at": null,
    "email": "user852@email.com",
    "is_admin": false,
    "phone_number": "01 23 45 67 89"
  }
}
```

**Status:** 201
### Request
```json
{
  "email": "user852@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "+33123456789"
}
```

### Response
```json
{
  "msg": "email \"user852@email.com\" is already taken."
}
```

**Status:** 422

## POST /api/auth/login
Login and get a token.

### Request
```json
{
  "email": "user852@email.com",
  "password": "password"
}
```

### Response
```json
{
  "token": "9-7-cb1861cffaf819a71a70a1875ebde5ec1229c253bac028cafaec38829948f80c",
  "user": {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 7,
    "created_at": "2022-11-30 00:29:05.320363",
    "updated_at": null,
    "email": "user852@email.com",
    "is_admin": false,
    "phone_number": "01 23 45 67 89"
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
  "email": "user852@email.com",
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
    "created_at": "2022-11-30 00:16:36.286194",
    "updated_at": null,
    "email": "user371@email.com",
    "is_admin": false,
    "phone_number": "01 23 45 67 89"
  },
  {
    "firstname": null,
    "lastname": null,
    "id": 2,
    "created_at": "2022-11-30 00:16:36.644401",
    "updated_at": null,
    "email": "user175@email.com",
    "is_admin": false,
    "phone_number": null
  },
  {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 4,
    "created_at": "2022-11-30 00:28:13.521740",
    "updated_at": null,
    "email": "user310@email.com",
    "is_admin": false,
    "phone_number": "01 23 45 67 89"
  },
  {
    "firstname": null,
    "lastname": null,
    "id": 5,
    "created_at": "2022-11-30 00:28:13.923592",
    "updated_at": null,
    "email": "user903@email.com",
    "is_admin": false,
    "phone_number": null
  },
  {
    "firstname": null,
    "lastname": null,
    "id": 6,
    "created_at": "2022-11-30 00:28:14.513524",
    "updated_at": null,
    "email": "admin@localhost",
    "is_admin": true,
    "phone_number": null
  },
  {
    "firstname": "prenom",
    "lastname": "nom",
    "id": 7,
    "created_at": "2022-11-30 00:29:05.320363",
    "updated_at": null,
    "email": "user852@email.com",
    "is_admin": false,
    "phone_number": "01 23 45 67 89"
  },
  {
    "firstname": null,
    "lastname": null,
    "id": 8,
    "created_at": "2022-11-30 00:29:05.695157",
    "updated_at": null,
    "email": "user438@email.com",
    "is_admin": false,
    "phone_number": null
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
  "id": 6,
  "created_at": "2022-11-30 00:28:14.513524",
  "updated_at": null,
  "email": "admin@localhost",
  "is_admin": true,
  "phone_number": null
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
  "created_at": "2022-11-30 00:16:36.286194",
  "updated_at": null,
  "email": "user371@email.com",
  "is_admin": false,
  "phone_number": "01 23 45 67 89"
}
```

**Status:** 200

## DELETE /api/users/3
Delete a user

> :police_car: This request requires admin privileges. An user must be authenticated via a token and have the `is_admin` flag set to `True`.
### Response
```json
{
  "msg": "The requested resource was not found"
}
```

**Status:** 404

## GET /api/listings
Get the list of listings

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[]
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
[]
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
[]
```

**Status:** 200

## GET /api/listings/1
Get a specific listing

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
{
  "msg": "The requested resource was not found"
}
```

**Status:** 404

## GET /api/listings/1/matches
Get the matching listings for an organ

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
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
  "created_at": "2022-11-30 00:29:06.379944",
  "updated_at": null,
  "name": "Chat name",
  "creator_id": 6
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
    "created_at": "2022-11-30 00:29:06.379944",
    "updated_at": null,
    "name": "Chat name",
    "creator_id": 6
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
  "created_at": "2022-11-30 00:29:06.379944",
  "updated_at": null,
  "name": "Chat name",
  "creator_id": 6
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
  "id": 3,
  "created_at": "2022-11-30 00:29:06.438261",
  "updated_at": null,
  "content": "Hello world!",
  "chat_id": 1,
  "sender_id": 6
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
      "created_at": "2022-11-30 00:29:06.379944",
      "updated_at": null,
      "name": "Chat name",
      "creator_id": 6
    },
    "last_message": {
      "id": 3,
      "created_at": "2022-11-30 00:29:06.438261",
      "updated_at": null,
      "content": "Hello world!",
      "chat_id": 1,
      "sender_id": 6
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
    "id": 3,
    "created_at": "2022-11-30 00:29:06.438261",
    "updated_at": null,
    "content": "Hello world!",
    "chat_id": 1,
    "sender_id": 6
  }
]
```

**Status:** 200

## DELETE /api/chats/1
Delete a chat

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 204

