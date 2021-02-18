from typing import List
from fastapi import APIRouter, Depends, HTTPException
from db.mongo import db
from bson import ObjectId
from models.services import NewService, Service, ServiceVersion, ServiceResponse
from models.users import User
from util.auth import get_current_active_user, verify_role

import logging
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/services",
    tags=["Services"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[ServiceResponse])
async def get_all_services(current_user: User = Depends(get_current_active_user)):
    """
    Gets all services.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Viewer", "Editor", "Admin"])
    # Instantiate empty list.
    services = []
    # For each document returned from find().
    # We only want to find() documents in our account.
    # TODO: Need to additionally sort by the account's preferred environment order.
    for service in db.services.find({"account": current_user['account']}).sort([("application", 1), ("service", 1)]):
        # Convert the _id to a string.
        service['_id'] = str(service['_id'])
        # Append document to the list.
        services.append(service)
    # Log our list for debugging.
    logger.debug(services)
    # Return the list to the client.
    return services


@router.get("/{_id}", response_model=ServiceResponse)
async def get_one_service(_id: str, current_user: User = Depends(get_current_active_user)):
    """
    Gets a single service by id.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Viewer", "Editor", "Admin"])
    # Print item in request for debugging.
    logger.debug(_id)
    # Find our one document matching our id, in our current_user's account.
    try:
        service = db.services.find_one({"_id": ObjectId(_id), "account": current_user['account']})
        # Log our result for debugging.
        logger.debug(service)
    except Exception as e:
        # Log our exception for debugging.
        logger.error(e)
        raise HTTPException(status_code=404, detail=f"{_id} not found")
    # find_one() returns NoneType if not found, so we need to catch that case and Raise exception.
    if service is None:
        raise HTTPException(status_code=404, detail=f"{_id} not found")
    # Raise exception if id not found in service
    if '_id' not in service:
        raise HTTPException(status_code=404, detail=f"{_id} not found")
    # Convert the _id to a string.
    service['_id'] = str(service['_id'])
    # Print our document for debugging.
    logger.debug(service)
    # Return the document to the client.
    return service


@router.put("/")
async def create_service(body: NewService, current_user: User = Depends(get_current_active_user)):
    """
    Creates a new service.
    """
    resp = ''
    body_dict = body.dict()
    # Verify the user has the allowed role.
    verify_role(current_user, ["Editor", "Admin"])
    # Print item in request for debugging.
    logger.debug(f"body: {body_dict}")
    service_dict = {
        "account": current_user['account'],
        "service": body_dict['service'],
        "application": body_dict['application']
    }
    # Query the db to see if already exists.
    if db.services.find_one(service_dict) is not None:
        # Raise exception if already exists.
        raise HTTPException(status_code=400, detail="Service already exists in this account.")

    # Attempt to insert item.
    try:
        resp = db.services.insert_one(service_dict)
    except Exception as e:
        # Log our exception for debugging.
        logger.error(f"e: {e}")
        # Raise exception if failed to insert.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    return {'_id': str(resp.inserted_id)}


# TODO: Not done yet, query existing object, make a nice update, then perform db.update()
@router.post("/")
async def update_service(body: Service, current_user: User = Depends(get_current_active_user)):
    """
    Updates an existing service.
    """
    body_dict = body.dict()
    response = ''
    # Verify the user has the allowed role.
    verify_role(current_user, ["Editor", "Admin"])
    # Log item in request for debugging.
    logger.debug(f"body: {body_dict}")
    # Attempt to update an item, passing upsert which will create object if does not exist.
    try:
        response = db.services.update(
            {"account": current_user['account'], "service": body_dict['service']},
            body_dict,
            upsert=True
        )
    except Exception as e:
        # Log our exception for debugging.
        logger.error(f"e: {e}")
        # Raise exception if failed to insert.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    return response


@router.delete("/{_id}")
async def delete_service(_id, current_user: User = Depends(get_current_active_user)):
    """
    Deletes a user
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Editor", "Admin"])
    # Query db for service id in the requester account.
    service = db.services.find_one({"_id": ObjectId(_id), "account": current_user['account']})
    if service is None:
        # Raise exception if service not found.
        raise HTTPException(status_code=404, detail="Service Not Found.")
    # Delete the service.
    db.services.delete_one({"_id": ObjectId(_id), "account": current_user['account']})
    # Return the inserted user id.
    return {'_id': _id, 'detail': 'Service deleted successfully.'}
