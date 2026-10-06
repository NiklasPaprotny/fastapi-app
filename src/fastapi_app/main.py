from fastapi import Depends, FastAPI, HTTPException
from fastapi_app.database import db
from .models.auth import Token, LoginRequest
from .models.user import User
from .auth.jwt import create_access_token
from fastapi_app.auth.dependency import get_current_user

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/user")
def read_users():
    return db.get_all_users()


@app.get("/user/{user_id}")
def read_user(user_id: int):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/user", status_code=201)
def create_user(user: User):
    created_user = db.create_user(user)
    return created_user

@app.post("/login", response_model=Token)
def login(username: str = Form(...), password: str = Form(...)):
    user = db.get_user_by_email(username)
    if not user or not password == str(user["age"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user["id"])})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    print
    return current_user