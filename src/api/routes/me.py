import logging
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from util.auth import get_current_active_user
from models.users import UpdateUserAsSelf, User, UserResponse
from db.mongo import db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/me",
    tags=["Me"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Get requester user account.
    """
    # All users are able to call this route, so we do not validate roles.
    # Log our user for debugging.
    logger.debug(f"me: {current_user}")
    # We already get current_user so we just return that.
    return current_user


@router.post("/")
async def update_me(user_updates: UpdateUserAsSelf, current_user: User = Depends(get_current_active_user)):
    """
    Update requester user account with allowed properties.
    """
    logger.debug(f'current_user: {current_user}')
    logger.debug(f'user_updates: {user_updates}')
    # Convert our user_updates to a dict.
    user_updates_dict = dict(user_updates)
    # Set our updates.
    updates = {}
    # Loop through the payload for non empty values.
    for key in user_updates_dict:
        if user_updates_dict[key] is not None:
            # Add to the updates dict.
            updates[key] = user_updates_dict[key]
    # Check if our updates dict is empty since all fields are optional.
    if not updates:
        # Skip the DB call, we aren't making any updates.
        return {"modified_count": "0"}
    # Create our update command from our updates dict.
    update_command = {"$set": updates}
    # Set our query for the update.
    query = {"_id": ObjectId(current_user["_id"])}
    # Call our update_user_in_db function.
    response = update_user_in_db(query, update_command)
    # Return the response.
    return response


def update_user_in_db(query, update_command):
    """
    Updates the user in the database.
    """
    try:
        # Put the new user_dict in the db.
        resp = db.users.update_one(query, update_command)
        # Log for debugging.
        logger.debug(f"resp: {resp}")
        # Return the modified count.
        return {'modified_count': str(resp.modified_count)}
    except Exception as e:
        # Log error
        logger.error(f"Exception: {e}")
        # Raise exception if user not found.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
