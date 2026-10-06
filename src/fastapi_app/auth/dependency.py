# auth/dependency.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from fastapi_app.auth.jwt import decode_access_token
from fastapi_app.database import db
print("dependency.py loaded")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    print("reached")
    payload = decode_access_token(token)
    print(payload)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    user = db.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user