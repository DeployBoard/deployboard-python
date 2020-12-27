from typing import List
from fastapi import APIRouter, Depends, HTTPException
from db.mongo import db
from bson import ObjectId
from models.logs import NewLog, Log, LogResponse
from models.users import User
from util.auth import get_current_active_user, verify_role

import logging
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[LogResponse])
async def get_all_logs(current_user: User = Depends(get_current_active_user)):
    """
    Gets all logs.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Viewer", "Editor", "Admin"])
    # Instantiate empty list.
    logs = []
    # For each document returned from find().
    # We only want to find() documents in our account. Sorted descending by timestamp.
    for log in db.logs.find({"account": current_user['account']}).sort("timestamp", -1):
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
        raise HTTPException(status_code=404, detail=f"{_id} not found")
    # find_one() returns NoneType if not found, so we need to catch that case and Raise exception.
    if log is None:
        raise HTTPException(status_code=404, detail=f"{_id} not found")
    # Raise exception if id not found in service
    if '_id' not in log:
        raise HTTPException(status_code=404, detail=f"{_id} not found")
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
