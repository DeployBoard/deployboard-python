from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from util.auth import authenticate_user, create_access_token, get_current_active_user, verify_role
from models.auth import Token
from models.users import User

from datetime import datetime, timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(
    tags=["Auth"],
    responses={404: {"description": "Not found"}}
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['_id']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
