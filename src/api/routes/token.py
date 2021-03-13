from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from util.auth import authenticate_user, create_access_token
from models.auth import Token
from datetime import timedelta

import logging
logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours

router = APIRouter(
    prefix="/token",
    tags=["Auth"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=Token)
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
