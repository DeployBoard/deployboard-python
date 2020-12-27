from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from util.auth import get_current_active_user, verify_role
from models.users import CreateUser, User, UserResponse, UserInDB
from db.mongo import db

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: User = Depends(get_current_active_user)):
    """
    Gets all users from the requester account.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])  # TODO: this func is called for every route find a way to better do this
    # Instantiate empty list.
    users = []
    # For each user returned from find().
    for user in db.users.find({"account": current_user['account']}):
        # Convert the _id to a string.
        user['_id'] = str(user['_id'])
        # Our response_model excludes hashed_password, but delete from user dict for extra safety.
        if 'hashed_password' in user:
            del user['hashed_password']
        # Append user to the list.
        users.append(user)
    # Log our list for debugging.
    logger.debug(users)
    # Return the list to the client. Our response_model of UserResponse includes _id, but excludes hashed_password.
    return users


@router.get("/{_id}", response_model=UserResponse)
async def get_user(_id, current_user: User = Depends(get_current_active_user)):
    """
    Gets specific users from the requester account.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])
    # Query db for user id in the requester account.
    user = db.users.find_one({"_id": ObjectId(_id), "account": current_user['account']})
    if user is None:
        # Raise exception if user not found.
        raise HTTPException(status_code=404, detail="User Not Found.")
    # Convert the _id to a string.
    user['_id'] = str(user['_id'])
    # Our response_model excludes hashed_password, but delete from user dict for extra safety.
    if 'hashed_password' in user:
        del user['hashed_password']
    # Log our list for debugging.
    logger.debug(user)
    # Return the list to the client. Our response_model of UserResponse includes _id, but excludes hashed_password.
    return user


@router.post("/")
async def create_user(user: CreateUser, current_user: User = Depends(get_current_active_user)):
    """
    Creates a new user
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])
    # Query the db to see if the user already exists.
    # Currently email needs to be unique within the entire users collection. Current auth looks for the account
    # associated with the user's email address. If an email were to exist twice, but for different accounts, the user
    # could potentially to gain access to the other account. This would be okay in theory because the user was granted
    # access to both accounts, but we have not accounted for this yet in auth validation, and we are not sure this is
    # even a use case we would like to support. A single email associated to a single account.
    # TODO: I would like to not return a message that says the user exists in another account, because it could be a way
    # TODO: for attackers to determine valid user/email addresses. How can we make this better without revealing the
    # TODO: user already exists?
    if db.users.find_one({"email": user.email}) is not None:
        # Raise exception if user already exists
        raise HTTPException(status_code=400, detail="User already exists, may be associated with another account.")

    # We can't insert the model, so we have to convert to dict.
    user_dict = user.dict()
    # We don't accept account in the payload, so append the current_user's account to the new user_dict.
    user_dict['account'] = current_user['account']
    # Put the new user_dict in the db.
    resp = db.users.insert_one(user_dict)
    # Return the inserted user id.
    return {'_id': str(resp.inserted_id)}


@router.delete("/{_id}")
async def delete_user(_id, current_user: User = Depends(get_current_active_user)):
    """
    Deletes a user
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])  # TODO: find a way to build this into the get_current_active_user func
    logger.debug(current_user)
    # Can not delete yourself.
    if _id == current_user['_id']:
        # Raise exception if user is trying to delete themself.
        raise HTTPException(status_code=400, detail="Can not delete yourself.")

    # Query db for user id in the requester account.
    user = db.users.find_one({"_id": ObjectId(_id), "account": current_user['account']})
    if user is None:
        # Raise exception if user not found.
        raise HTTPException(status_code=404, detail="User Not Found.")
    # Delete the user.
    db.users.delete_one({"_id": ObjectId(_id), "account": current_user['account']})
    # Return the deleted user id.
    return {'_id': _id, 'detail': 'User deleted successfully.'}
