# Upgrading to 2.0

## Breaking changes

The conversion from FastAPI to Flask came with some breaking changes, here is a
list

If you notice any breaking change not listed here, open a PR to add it

If you disagree with some changes, open an issue and label it as "discussion"

### Public changes

_Changes that impacts the API consumers_

- `POST /auth/` -> `POST /auth/login`
- `POST /users/` -> `POST /auth/register`
- Listing.donor (boolean) removed in favor of Listing.type of type Listing.Type,
  being either donor or patient
- Almost all fields in the Listing models have been renamed to be more Pythonic
- Invitations removed (again), let's consider them out of scope for now, if they
  want the app to only be available to their team they can use a private
  connection
- Roles system removed: We only had 2 (admin and default), and there weren't
  cases of needing to update them dynamically, so we regressed to a simple
  `is_admin` flag on users
- Removed chats: out of scope
- Removed calendar: out of scope
- Action Log has been removed, if reimplemented, it should be done using a
  **temporal database** or at least **NoSQL**, and should be externalized

### Internal changes

_Changes that impacts the development process_
