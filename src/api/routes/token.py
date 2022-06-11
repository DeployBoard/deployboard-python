import logging
from datetime import timedelta
from urllib.parse import parse_qs

from fastapi import APIRouter, HTTPException, Request
from models.auth import Token
from util.auth import authenticate_user, create_access_token
from util.sso.okta import verify_okta_code

logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours

router = APIRouter(
    prefix="/token", tags=["Auth"], responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=Token)
async def login_for_access_token(request: Request):
    logger.debug(f"request.headers: {request.headers}")

    if not request.headers["Authorization"]:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header with login method.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_method = request.headers["Authorization"].split(" ")[0]
    logger.debug(f"auth_method: {auth_method}")

    # Get the body as bytes.
    data_bytes = await request.body()
    # If we don't have a body, raise exception.
    if not data_bytes:
        raise HTTPException(
            status_code=401,
            detail="No body.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # convert the data_bytes to a string.
    data = data_bytes.decode("utf-8")
    # Parse the body data to a dictionary.
    payload = parse_qs(data)
    logger.debug(f"data: {payload}")

    if auth_method == "Basic":
        # We are Basic username/password auth.
        logger.debug(
            f"username: {payload['username'][0]}, password: {payload['password'][0]}"
        )
        user = authenticate_user(payload["username"][0], payload["password"][0])

    # Get login method local or sso from the request and route to the proper method.
    if auth_method == "Okta":
        logger.debug(f"token: {request.headers['authorization']}")
        logger.debug(f"okta_code: {payload['okta_code'][0]}")
        # Verify our Okta Code and get user info.
        user = verify_okta_code(payload["okta_code"][0])
        logger.debug(f"user: {user}")

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["_id"], "email": user["email"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
