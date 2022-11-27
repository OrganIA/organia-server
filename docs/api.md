# API Documentation
Generated on: 2022-11-27 at 23:21:31

- [GET /api/](#get--api-)
- [POST /api/auth/login](#post--api-auth-login)
- [POST /api/auth/register](#post--api-auth-register)
- [GET /api/users](#get--api-users)
- [GET /api/users/me](#get--api-users-me)
- [GET /api/users/1](#get--api-users-1)
- [DELETE /api/users/3](#delete--api-users-3)
- [GET /api/listings](#get--api-listings)
- [GET /api/listings/1](#get--api-listings-1)
- [GET /api/listings/1/matches](#get--api-listings-1-matches)
- [GET /api/chats](#get--api-chats)
- [GET /api/chats/1](#get--api-chats-1)
- [POST /api/chats](#post--api-chats)
- [GET /api/chats/messages/latest](#get--api-chats-messages-latest)
- [GET /api/chats/1/messages](#get--api-chats-1-messages)
- [POST /api/chats/1/messages](#post--api-chats-1-messages)
- [DELETE /api/chats/1](#delete--api-chats-1)


## GET /api/
Information about the server, such as the version or the OS.
Useful to check if the server is up, or to check if it is running
the latest version.

### Response
**Status:** 403

## POST /api/auth/login
Login and get a token.

### Request
```json
{
  "email": "user@email.com",
  "password": "password"
}
```

### Response
**Status:** 403
### Request
```json
{
  "email": "user@email.com",
  "password": "not-the-password"
}
```

### Response
**Status:** 403

## POST /api/auth/register
Register a new user, response should be the same as login, so no need to
login after registering.

### Request
```json
{
  "email": "user255@email.com",
  "password": "password",
  "firstname": "prenom",
  "lastname": "nom",
  "phone_number": "123456789"
}
```

### Response
**Status:** 403
### Request
```json
{
  "email": "user@email.com",
  "password": "password"
}
```

### Response
**Status:** 403

## GET /api/users
List all users

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

## GET /api/users/me
Get info about the current user

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

## GET /api/users/1
Get info about a specific user

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

## DELETE /api/users/3
Delete a user

> :police_car: This request requires admin privileges. An user must be authenticated via a token and have the `is_admin` flag set to `True`.
### Response
**Status:** 403

## GET /api/listings
Get the list of listings

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403
### Request
```json
{
  "page": 2,
  "per_page": 10
}
```

### Response
**Status:** 403
### Request
```json
{
  "search": "jean"
}
```

### Response
**Status:** 403

## GET /api/listings/1
Get a specific listing

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

## GET /api/listings/1/matches
Get the matching listings for an organ

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

## GET /api/chats
Get all the users chats

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

## GET /api/chats/1
Get a specific chat

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

## POST /api/chats
Create a new chat

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "chat_name": "Chat name",
  "users_ids": [
    1,
    2
  ]
}
```

### Response
**Status:** 403

## GET /api/chats/messages/latest
Get all latest messages

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

## GET /api/chats/1/messages
Get all messages for a specific chat

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

## POST /api/chats/1/messages
Send a message

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Request
```json
{
  "content": "Hello world!",
  "sender_id": 1,
  "chat_id": 1
}
```

### Response
**Status:** 403

## DELETE /api/chats/1
Delete a chat

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
**Status:** 403

