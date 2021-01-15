from datetime import datetime
from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from util.auth import get_current_active_user, verify_role
from models.apikeys import CreateApiKey, ApiKeyResponse
from models.users import User
from db.mongo import db

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/apikeys",
    tags=["ApiKeys"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[ApiKeyResponse])
async def get_apikeys(current_user: User = Depends(get_current_active_user)):
    """
    Gets all api keys from the requester account.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])  # TODO: this func is called for every route find a way to better do this
    # Instantiate empty list.
    apikeys = []
    # For each user returned from find().
    for key in db.apikeys.find({"account": current_user['account']}):
        # Convert the _id to a string.
        key['_id'] = str(key['_id'])
        # Append user to the list.
        apikeys.append(key)
    # Log our list for debugging.
    logger.debug(apikeys)
    # Return the list to the client.
    return apikeys


@router.get("/{_id}", response_model=ApiKeyResponse)
async def get_apikey(_id, current_user: User = Depends(get_current_active_user)):
    """
    Gets specific api key from the requester account.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])
    # Query db for user id in the requester account.
    key = db.apikeys.find_one({"_id": ObjectId(_id), "account": current_user['account']})
    if key is None:
        # Raise exception if user not found.
        raise HTTPException(status_code=404, detail="User Not Found.")
    # Convert the _id to a string.
    key['_id'] = str(key['_id'])
    # Log our list for debugging.
    logger.debug(key)
    # Return the list to the client.
    return key


@router.post("/")
async def create_apikey(apikey: CreateApiKey, current_user: User = Depends(get_current_active_user)):
    """
    Creates a new api key
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])
    # Generate a timestamp for our created and modified timestamp attributes.
    timestamp = datetime.utcnow().timestamp()
    # We can't insert the model, so we have to convert to dict.
    apikey_dict = apikey.dict()
    # We don't accept account in the payload, so append the current_user's account to the new user_dict.
    apikey_dict['account'] = current_user['account']
    # Add created by current user.
    apikey_dict['created_by'] = current_user['email']
    # Add modified by current user since this is the beginning of history for this key.
    apikey_dict['modified_by'] = current_user['email']
    # Add created timestamp.
    apikey_dict['created_timestamp'] = timestamp
    # Add modified timestamp.
    apikey_dict['modified_timestamp'] = timestamp
    try:
        # Put the new apikey_dict in the db.
        resp = db.apikeys.insert_one(apikey_dict)
    except Exception as e:
        logger.error(f"Unexpected error occurred. {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred. {e}")
    # Return the inserted user id.
    return {'_id': str(resp.inserted_id)}


@router.delete("/{_id}")
async def delete_apikey(_id, current_user: User = Depends(get_current_active_user)):
    """
    Deletes an api key
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])  # TODO: find a way to build this into the get_current_active_user func
    # Log for debugging.
    logger.debug(current_user)
    # Query db for user id in the requester account.
    apikey = db.apikeys.find_one({"_id": ObjectId(_id), "account": current_user['account']})
    if apikey is None:
        # Raise exception if api key not found.
        raise HTTPException(status_code=404, detail="Api Key Not Found.")
    # Delete the api key.
    db.apikeys.delete_one({"_id": ObjectId(_id), "account": current_user['account']})
    # Return the deleted api key id.
    return {'_id': _id, 'detail': 'Api Key deleted successfully.'}
