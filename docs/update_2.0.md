# Upgrading to 2.0

The conversion from FastAPI to Flask came with some breaking changes, here is a list

- `POST /auth/` -> `POST /auth/login`
- `POST /users/` -> `POST /auth/register`
