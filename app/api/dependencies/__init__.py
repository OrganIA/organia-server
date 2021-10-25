from fastapi import Depends
from .logged_user import logged_user

logged_user = Depends(logged_user)