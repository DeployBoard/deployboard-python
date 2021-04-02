from datetime import datetime, timedelta
import logging
from bson import ObjectId

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.users import User
from models.auth import TokenData
from db.mongo import db
from util.config import config

logger = logging.getLogger(__name__)

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = config('APP_SECRET')
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# TODO: If we are leaving auto_error=False, we need to have some way to check for User or APIKey
#  and protect APIKeyOnly endpoints.
api_key_header = APIKeyHeader(name='X-API-Key', auto_error=False)


def authenticate_user(username: str, password: str):
    """
    Verifies a username and password match what is in the db and that the user is enabled.
    """
    logger.debug(SECRET_KEY)
    user = get_user_by_email(username)
    # If user is empty we want to return invalid username/password.
    if not user:
        logger.debug("No user found.")
        return False
    # If user is disabled we want to return invalid username/password.
    if not user['enabled']:
        logger.info(f"Disabled user: {username} attempted to log in.")
        return False
    # Convert the _id to a string.
    user['_id'] = str(user['_id'])
    # If user exists, but the password does not match, we want to return invalid username/password.
    if not verify_password(password + user['salt'] + config('DPB_PEPPER'), user['hashed_password']):
        logger.info(f"User: {username} incorrect password.")
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    logger.debug("Creating new token")
    # Set our data to encode.
    to_encode = data.copy()
    # Set our time to expire.
    expire = datetime.utcnow() + expires_delta
    # Add our new expire time to data to encode.
    to_encode.update({"exp": expire})
    # Encode the JWT with our data, secret key, and algorithm.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # Return our encoded JWT.
    return encoded_jwt


def verify_password(salted_peppered_password, hashed_password):
    logger.debug("Verifying password")
    return pwd_context.verify(salted_peppered_password, hashed_password)


def generate_password_hash(password, salt):
    logger.debug("Generating password hash")
    return pwd_context.hash(password + salt + config("DPB_PEPPER"))


def get_user_by_email(username):
    logger.debug("Querying mongo for user")
    user = db.users.find_one({"email": username})
    return user


def get_user_by_id(user_id):
    logger.debug("Querying mongo for user")
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    logger.debug(SECRET_KEY)
    logger.debug("Getting current user")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(payload)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(username=user_id)
    except JWTError:
        logger.debug(JWTError)
        raise credentials_exception
    logger.debug(token_data)
    user = get_user_by_id(token_data.username)
    if user is None:
        raise credentials_exception
    # If user is disabled we want to return invalid username/password.  # TODO: This is duplicate, maybe func this.
    if not user['enabled']:
        logger.info(f"User: {user['email']} is disabled, attempted to use credentials.")
        raise HTTPException(status_code=400, detail="Inactive user")  # TODO: maybe return something more generic in case of attacker.
    # Convert the _id to a string.
    user['_id'] = str(user['_id'])
    logger.debug(user)
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    # verify_role(current_user, allowed_roles)
    return current_user


def verify_role(user, allowed_roles):
    # Check if the user's role is allowed
    if user['role'] not in allowed_roles:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


def get_api_key_in_header(api_key: str = Security(api_key_header)):
    """
    Verifies the API Key in the header.
    """
    # Return the api key after we verified there is an api key in the header.
    return api_key


def verify_api_key(api_key):
    """
    Checks if api key is in our db and returns that object.
    """
    # See if the api_key is in our db.
    try:
        # Find our object in the db.
        api_key_object = db.apikeys.find_one({"_id": ObjectId(api_key)})
        # log for debugging.
        logger.debug(f"api_key_object: {api_key_object}")
    except Exception as e:
        # Log for debugging.
        logger.debug(f"exception: {e}")
        # Raise exception if error or not found.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    # If db returns no results, return 403
    if api_key_object is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials.")

    return api_key_object
