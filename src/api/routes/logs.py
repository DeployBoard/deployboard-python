from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from db.mongo import db
from bson import ObjectId
from models.logs import LogResponse
from models.users import User
from util.auth import get_current_active_user, verify_role

import logging
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
    responses={404: {"description": "Not found"}}
)


# TODO: Can we also allow filtering on custom field? custom: Optional[dict] = None
@router.get("/", response_model=List[LogResponse])
async def get_all_logs(application: Optional[str] = None,
                       service: Optional[str] = None,
                       environment: Optional[str] = None,
                       status: Optional[str] = None,
                       from_timestamp: Optional[float] = None,
                       to_timestamp: Optional[float] = None,
                       sort: Optional[int] = -1,
                       current_user: User = Depends(get_current_active_user)):
    """
    Gets all logs matching query string parameters if provided.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Viewer", "Editor", "Admin"])
    # Instantiate our query with account since we pull that from auth.
    query = {"account": current_user['account']}
    # Check for query string parameters and add them to query if exist.
    if application is not None:
        query['application'] = application
    if service is not None:
        query['service'] = service
    if environment is not None:
        query['environment'] = environment
    if status is not None:
        query['status'] = status
    # Check our complex timestamp situation
    if from_timestamp is not None and to_timestamp is not None:
        # Both from and to were passed so get timestamps between the two.
        query['timestamp'] = {"$gt": from_timestamp, "$lt": to_timestamp}
    elif from_timestamp is not None:
        # Only from was passed so check greater than that.
        query['timestamp'] = {"$gt": from_timestamp}
    elif to_timestamp is not None:
        # Only to was passed so check less than that.
        query['timestamp'] = {"$lt": to_timestamp}
    # Raise exception if sort is not -1 or 1.
    if sort not in [-1, 1]:
        raise HTTPException(status_code=400, detail=f"sort must be -1 or 1, provided {sort}")
    # Instantiate empty list.
    logs = []
    # For each document returned from find() sorted by timestamp in the direction provided.
    for log in db.logs.find(query).sort("timestamp", sort):
        # Convert the _id to a string.
        log['_id'] = str(log['_id'])
        # Append document to the list.
        logs.append(log)
    # Log our list for debugging.
    logger.debug(logs)
    # Return the list to the client.
    return logs


@router.get("/{_id}", response_model=LogResponse)
async def get_one_log(_id: str, current_user: User = Depends(get_current_active_user)):
    """
    Gets a single log by id.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Viewer", "Editor", "Admin"])
    # Print item in request for debugging.
    logger.debug(_id)
    # Find our one document matching our id, in our current_user's account.
    try:
        log = db.logs.find_one({"_id": ObjectId(_id), "account": current_user['account']})
        # Log our result for debugging.
        logger.debug(log)
    except Exception as e:
        # Log our exception for debugging.
        logger.error(e)
        raise HTTPException(status_code=404, detail=f"Log: {_id} not found")
    # find_one() returns NoneType if not found, so we need to catch that case and Raise exception.
    if log is None:
        raise HTTPException(status_code=404, detail=f"Log: {_id} not found")
    # Convert the _id to a string.
    log['_id'] = str(log['_id'])
    # Print our document for debugging.
    logger.debug(log)
    # Return the document to the client.
    return log


# Currently we have intentionally decided to not include a PUT/POST/DELETE method for the logs endpoint. We feel that
# the logs collection should be an immutable trail of the history of your environment. Providing a method to manipulate
# the data would invalidate the quality of the data. Of course manual manipulation is possible via direct access to the
# database, but that requires a much higher level of awareness of your decision before you touch the data.
