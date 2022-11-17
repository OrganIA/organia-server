# API Documentation
Generated on: 2022-11-17 at 02:15:55

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


## GET /api/
Information about the server, such as the version or the OS.
Useful to check if the server is up, or to check if it is running
the latest version.

### Response
```json
{
  "version": "fc20153",
  "time": 1668644155.832427,
  "datetime": "2022-11-17 01:15:55.832427",
  "software": {
    "flask": "2.2.2",
    "python": "3.10.8",
    "system": {
      "name": "Fedora Linux 36 (Workstation Edition)",
      "platform": "Linux",
      "release": "6.0.8-200.fc36.x86_64",
      "arch": "x86_64"
    }
  }
}
```

**Status:** 200

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
```json
{
  "token": "38-1-9e89fe28f07967622fe7c478401671f03492a2168e329536e2657cae9da89788",
  "user": "<User #1: created_at=2022-10-13 03:51:29.338146, updated_at=None, email=user@email.com, password=pbkdf2:sha256:260000$3aBqhnE4BJFJZ8Pl$99489c7e6e62a45df6e18b58acc303a4f651d398e14314e51b587ceab1773f95, is_admin=False>"
}
```

**Status:** 200
### Request
```json
{
  "email": "user@email.com",
  "password": "no-the-password"
}
```

### Response
```json
{
  "msg": "Password mismatch"
}
```

**Status:** 422

## POST /api/auth/register
Register a new user, response should be the same as login, so no need to
login after registering.

### Request
```json
{
  "email": "user12@email.com",
  "password": "password"
}
```

### Response
```json
{
  "token": "39-13-5a159772eed9cb147f06eb3ad7864247be41d605c25f87d31745b2908be85185",
  "user": "<User #13: created_at=2022-11-17 01:15:56.339184, updated_at=None, email=user12@email.com, password=pbkdf2:sha256:260000$fdsBGhmMVCtZgvmK$b7f0ac9cb557de516ea8ba82fd399b607280f49bd70c294e5a45cb7cfb3e377b, is_admin=False>"
}
```

**Status:** 201
### Request
```json
{
  "email": "user@email.com",
  "password": "password"
}
```

### Response
```json
{
  "msg": "email \"user@email.com\" is already taken."
}
```

**Status:** 422

## GET /api/users
List all users

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  "<User #1: created_at=2022-10-13 03:51:29.338146, updated_at=None, email=user@email.com, password=pbkdf2:sha256:260000$3aBqhnE4BJFJZ8Pl$99489c7e6e62a45df6e18b58acc303a4f651d398e14314e51b587ceab1773f95, is_admin=False>",
  "<User #2: created_at=2022-11-16 19:04:54.362278, updated_at=None, email=admin@localhost, password=None, is_admin=True>",
  "<User #4: created_at=2022-11-17 00:55:00.325792, updated_at=None, email=user383@email.com, password=pbkdf2:sha256:260000$2xAHb6J6Oz1EMm5U$ef5edcc6c8e57a4183d5ecb930c3cf6002c23d2b94d189c59f274eb7b2c48d77, is_admin=False>",
  "<User #5: created_at=2022-11-17 00:57:17.048997, updated_at=None, email=user334@email.com, password=pbkdf2:sha256:260000$Z6kjkJdxDD5sRxpb$6d956b63cf830b6a2b7cf9f860869eda76eed043556f18f3de619bdb7469e85b, is_admin=False>",
  "<User #6: created_at=2022-11-17 00:58:17.767770, updated_at=None, email=user958@email.com, password=pbkdf2:sha256:260000$6omUteYVtzF8zz5c$c5bcb9dbbb9b4bbf38b09ad1fa31521af9d3c5ff9a629a039b4194f8a8a2611e, is_admin=False>",
  "<User #7: created_at=2022-11-17 01:02:27.162755, updated_at=None, email=user68@email.com, password=pbkdf2:sha256:260000$sMfGYnMQM9xni8gg$f2bbf4c1289f536c22846b92ad396db6976d78e54d25e16f4203e2b92da8e90a, is_admin=False>",
  "<User #8: created_at=2022-11-17 01:06:09.181881, updated_at=None, email=user676@email.com, password=pbkdf2:sha256:260000$YFGBvXyzmfQ11LrX$9a71ebef03220a1d68e211852f1720fda291035a56d7f136f48b0805bce30b08, is_admin=False>",
  "<User #9: created_at=2022-11-17 01:09:55.053135, updated_at=None, email=user428@email.com, password=pbkdf2:sha256:260000$R0w3FWriaJMdzzuL$57aeb6e205b88a0db4c7b66033937bc71ad85ec6680573190e6f718623529d53, is_admin=False>",
  "<User #10: created_at=2022-11-17 01:10:45.081153, updated_at=None, email=user377@email.com, password=pbkdf2:sha256:260000$f40ayEc4d5pAJGcl$a40dda91e2f394aed5439b0aae037df7b7a2ed0543281718d7ea75b2eb602d94, is_admin=False>",
  "<User #11: created_at=2022-11-17 01:13:52.846548, updated_at=None, email=user583@email.com, password=pbkdf2:sha256:260000$W5HvyaTKo8jFwBns$8c45276706f285efdcee39516ed1d2908461b63c070fa9a7178fdcfc367bf246, is_admin=False>",
  "<User #12: created_at=2022-11-17 01:14:48.081630, updated_at=None, email=user271@email.com, password=pbkdf2:sha256:260000$FPjIPIUaH0GfBKQ0$cfd25a4a0a88c03801457ccc606e4128cd04b7a6880f2bcae6f9293ea28363e4, is_admin=False>",
  "<User #13: created_at=2022-11-17 01:15:56.339184, updated_at=None, email=user12@email.com, password=pbkdf2:sha256:260000$fdsBGhmMVCtZgvmK$b7f0ac9cb557de516ea8ba82fd399b607280f49bd70c294e5a45cb7cfb3e377b, is_admin=False>"
]
```

**Status:** 200

## GET /api/users/me
Get info about the current user

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
"<User #2: created_at=2022-11-16 19:04:54.362278, updated_at=None, email=admin@localhost, password=None, is_admin=True>"
```

**Status:** 200

## GET /api/users/1
Get info about a specific user

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
"<User #1: created_at=2022-10-13 03:51:29.338146, updated_at=None, email=user@email.com, password=pbkdf2:sha256:260000$3aBqhnE4BJFJZ8Pl$99489c7e6e62a45df6e18b58acc303a4f651d398e14314e51b587ceab1773f95, is_admin=False>"
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
[
  "<Listing #1: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #2: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #3: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #4: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #5: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #6: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #7: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #8: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #9: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #10: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #11: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #12: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>"
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
  "<Listing #1: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #2: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #3: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #4: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #5: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #6: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #7: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #8: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #9: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #10: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #11: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #12: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>"
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
  "<Listing #1: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #2: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #3: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #4: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #5: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #6: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #7: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #8: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #9: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #10: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #11: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>",
  "<Listing #12: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>"
]
```

**Status:** 200

## GET /api/listings/1
Get a specific listing

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
"<Listing #1: notes=None, type=None, organ=None, tumors_number=0, biggest_tumor_size=None, alpha_fetoprotein=None, is_under_dialysis=None, dialysis_start_date=None, dialysis_end_date=None, is_retransplantation=None, arf_date=None, transplantation_date=None, re_registration_date=None, A=None, B=None, DR=None, DQ=None, person_id=None, hospital_id=None>"
```

**Status:** 200

## GET /api/listings/1/matches
Get the matching listings for an organ

> :lock: This request requires authentication. Pass `Bearer: the-token` in the `Authorization` header.
### Response
```json
[
  {
    "listing": {
      "id": 4,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.9214515271124273
  },
  {
    "listing": {
      "id": 8,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.8987267364346623
  },
  {
    "listing": {
      "id": 7,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.7547437005048416
  },
  {
    "listing": {
      "id": 9,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.7275920992118209
  },
  {
    "listing": {
      "id": 12,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.5973090738830306
  },
  {
    "listing": {
      "id": 11,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.5744453743344891
  },
  {
    "listing": {
      "id": 3,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.3957538293059544
  },
  {
    "listing": {
      "id": 10,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.2920772751343629
  },
  {
    "listing": {
      "id": 2,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.209111349630123
  },
  {
    "listing": {
      "id": 5,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.09990506963442891
  },
  {
    "listing": {
      "id": 6,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.08161969062311514
  },
  {
    "listing": {
      "id": 1,
      "type": null,
      "notes": null,
      "organ": null,
      "person_id": null,
      "hospital_id": null
    },
    "score": 0.05294566062437822
  }
]
```

**Status:** 200

