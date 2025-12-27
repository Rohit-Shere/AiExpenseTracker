from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from backend.security import (
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)
from backend.users import create_user, get_user_by_email, get_user_by_id
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# =======================
# Schemas
# =======================

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# =======================
# Routes
# =======================

@router.post("/signup")
def signup(data: SignupRequest):
    existing = get_user_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(data.name, data.email, data.password)
    token = create_access_token({"sub": str(user["id"])})

    return {"access_token": token, "user": user}

@router.post("/login")
def login(data: LoginRequest):
    user = get_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id, name, email, hashed = user
    if not verify_password(data.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user_id)})

    return {
        "access_token": token,
        "user": {"id": user_id, "name": name, "email": email}
    }

# =======================
# Get Current User
# =======================

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {"id": user[0], "name": user[1], "email": user[2]}

@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return current_user
