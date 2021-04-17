import logging
import secrets
from datetime import datetime, timedelta
from typing import List

from bson import ObjectId
from db.mongo import db
from fastapi import APIRouter, Depends, HTTPException
from models.users import CreateUser, UpdateUserAsAdmin, User, UserResponse
from util.auth import generate_password_hash, get_current_active_user, verify_role
from util.password_policy import check_password_policy
from util.response import check_response

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users", tags=["Users"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: User = Depends(get_current_active_user)):
    """
    Gets all users from the requester account.
    """
    # Verify the user has the allowed role.
    verify_role(
        current_user, ["Admin"]
    )  # TODO: this func is called for every route find a way to better do this
    # Instantiate empty list.
    users = []
    # For each user returned from find().
    for user in db.users.find({"account": current_user["account"]}):
        # Convert the _id to a string.
        user["_id"] = str(user["_id"])
        # Remove hashed_password and salt.
        user.pop("hashed_password", None)
        user.pop("salt", None)
        # Check our user for unintended data.
        validated_user = check_response(current_user, user)
        # Append validated_user to the list.
        users.append(validated_user)
    # Log our list for debugging.
    logger.debug(users)
    # Return the list to the client. Our response_model of UserResponse includes _id,
    # but excludes hashed_password.
    return users


@router.get("/{_id}", response_model=UserResponse)
async def get_user(_id, current_user: User = Depends(get_current_active_user)):
    """
    Gets specific users from the requester account.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])
    # Query db for user id in the requester account.
    user = db.users.find_one({"_id": ObjectId(_id), "account": current_user["account"]})
    if user is None:
        # Raise exception if user not found.
        raise HTTPException(status_code=404, detail="User not found.")
    # Convert the _id to a string.
    user["_id"] = str(user["_id"])
    # Log our user for debugging.
    logger.debug(f"user: {user}")
    # Remove hashed_password and salt.
    user.pop("hashed_password", None)
    user.pop("salt", None)
    # Check our user for unintended data.
    validated_user = check_response(current_user, user)
    # Log our validated_response for debugging.
    logger.debug(validated_user)
    # Return the list to the client. Our response_model of UserResponse includes _id,
    # but excludes hashed_password.
    return validated_user


@router.put("/")
async def create_user(
    user: CreateUser, current_user: User = Depends(get_current_active_user)
):
    """
    Creates a new user
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])
    # Query the db to see if the user already exists.
    # Currently email needs to be unique within the entire users collection. Current
    # auth looks for the account associated with the user's email address. If an email
    # were to exist twice, but for different accounts, the user could potentially to
    # gain access to the other account. This would be okay in theory because the user
    # was granted access to both accounts, but we have not accounted for this yet in
    # auth validation, and we are not sure this is even a use case we would like to
    # support. A single email associated to a single account.
    # TODO: I would like to not return a message that says the user exists in another
    #  account, because it could be a way for attackers to determine valid user/email
    #  addresses. How can we make this better without revealing the user already exists?
    if db.users.find_one({"email": user.email}) is not None:
        # Raise exception if user already exists
        raise HTTPException(
            status_code=400,
            detail="User already exists, may be associated with another account.",
        )

    # We can't insert the model, so we have to convert to dict.
    user_dict = user.dict()
    # We don't accept account in the payload, so append the current_user's account
    # to the new user_dict.
    user_dict["account"] = current_user["account"]
    # We get the requesting user data from current_user.
    user_dict["created_by"] = current_user["email"]
    user_dict["modified_by"] = current_user["email"]
    # Check to see if the password meets the account's policy.
    check_password_policy(user_dict["account"], user_dict["password"])
    # Generate an epoch to use for created and modified timestamp.
    ts = datetime.utcnow().timestamp()
    user_dict["created_timestamp"] = ts
    user_dict["modified_timestamp"] = ts
    # Generate an epoch to use for expiration timestamp.
    # Set the time in the past that way it forces user to change password on next login.
    expires = (datetime.utcnow() - timedelta(days=1)).timestamp()
    user_dict["password_expires"] = expires
    # Generate a salt for the user.
    user_dict["salt"] = secrets.token_hex(16)
    # Hash our password + salt + pepper.
    user_dict["hashed_password"] = generate_password_hash(
        user_dict["password"], user_dict["salt"]
    )
    # Now that we have the hashed_password, we need to remove the plain text password
    # from the user_dict.
    user_dict.pop("password", None)
    # Put the new user_dict in the db.
    resp = db.users.insert_one(user_dict)
    # Return the inserted user id.
    return {"_id": str(resp.inserted_id)}


@router.patch("/{_id}")
async def update_user(
    _id, user: UpdateUserAsAdmin, current_user: User = Depends(get_current_active_user)
):
    """
    Updates specific user from the requester account.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])
    # We can't insert the model, so we have to convert to dict.
    user_dict = user.dict()
    # Set our updates.
    updates = {}
    # Loop through the payload for non empty values.
    for key in user_dict:
        if user_dict[key] is not None:
            # Add to the updates dict.
            updates[key] = user_dict[key]
    # Log for debugging.
    logger.debug(f"updates: {updates}")
    # Check if our updates dict is empty since all fields are optional.
    if not updates:
        # Skip the DB call, we aren't making any updates.
        return {"modified_count": "0"}
    # Handle if password was passed
    if "password" in updates:
        # Check to see if the password meets the account's policy.
        check_password_policy(current_user["account"], updates["password"])
        # Generate an epoch to use for expiration timestamp.
        # Set the time in the past that way it forces user to change password
        # on next login.
        expires = (datetime.utcnow() - timedelta(days=1)).timestamp()
        updates["password_expires"] = expires
        # Generate a new salt for the user.
        updates["salt"] = secrets.token_hex(16)
        # Hash our password + salt + pepper.
        updates["hashed_password"] = generate_password_hash(
            updates["password"], updates["salt"]
        )
        # Now that we have the hashed_password, we need to remove the plain text
        # password from the user_dict.
        updates.pop("password", None)
    # Make our update request to the db.
    response = db.users.update_one({"_id": ObjectId(_id)}, {"$set": updates})
    # Log response for debugging.
    logger.debug(f"user: {response.raw_result}")
    if response.matched_count == 0:
        # Raise exception if user not found.
        raise HTTPException(status_code=404, detail="User not found.")
    # Return success.
    return {"status": "Updated successfully."}


@router.delete("/{_id}")
async def delete_user(_id, current_user: User = Depends(get_current_active_user)):
    """
    Deletes a user
    """
    # Verify the user has the allowed role.
    verify_role(
        current_user, ["Admin"]
    )  # TODO: find a way to build this into the get_current_active_user func
    logger.debug(current_user)
    # Can not delete yourself.
    if _id == current_user["_id"]:
        # Raise exception if user is trying to delete themself.
        raise HTTPException(status_code=400, detail="Can not delete yourself.")

    # Query db for user id in the requester account.
    user = db.users.find_one({"_id": ObjectId(_id), "account": current_user["account"]})
    if user is None:
        # Raise exception if user not found.
        raise HTTPException(status_code=404, detail="User not found.")
    # Delete the user.
    db.users.delete_one({"_id": ObjectId(_id), "account": current_user["account"]})
    # Return the deleted user id.
    return {"_id": _id, "detail": "User deleted successfully."}
