from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from db.mongo import db
from models.deployments import DeploymentRequest
from util.auth import get_api_key_in_header, verify_api_key, verify_role

import logging
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/deploy",
    tags=["Deploy"],
    responses={404: {"description": "Not found"}}
)


# This endpoint is protected by API key, not by JWT.
@router.api_route("/", methods=["PUT", "POST"])
async def create_or_update_deployment(body: DeploymentRequest, api_key: str = Depends(get_api_key_in_header)):
    """
    Creates a new deployment, or updates an existing deployment.
    """
    # Verify our api key is in the db.
    api_key_object = verify_api_key(api_key)
    # Log for debugging.
    logger.debug(f"api_key_object: {api_key_object}")
    # Verify our api key has the allowed role.
    verify_role(api_key_object, ["Editor", "Admin"])
    # Convert our body from pydantic model to dict.
    deployment = body.dict()
    # Add timestamp as utc epoch.
    deployment['timestamp'] = datetime.utcnow().timestamp()
    # Add the account from our api key.
    deployment['account'] = api_key_object['account']
    # Try to insert our object into the logs db.
    try:
        # Insert object into the logs db.
        result = db.logs.insert_one(deployment)
        # Log the inserted id for debugging.
        logger.debug(f"insert_logs_result: {result.inserted_id}")
    except Exception as e:
        logger.debug(f"exception: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {e}")

    # TODO: Generate the hashed value for the record in the logs table.
    # TODO: Query (or upsert maybe?) services table to find our service that matches our account+application
    #  and update the environment in the object with this new deployment data.
    #  If a system does not already exist, create a new one for the user (this is where upsert might be better)
    #   But we don't want to overwrite an existing system data, so upsert might be bad idea.
    #   It might be safer to just query the item, update it here within this function, then write back the new object.

    # TODO: return "success" or something to let the user know we inserted the items successfully.

    return [body, api_key]
