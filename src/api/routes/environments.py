import logging
from typing import List

from db.mongo import db
from fastapi import APIRouter, Depends, HTTPException
from models.environments import UpdateEnvironment
from models.users import User
from util.auth import get_current_active_user, verify_role
from util.response import check_response

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/environments",
    tags=["Environments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[str])
async def get_environments(current_user: User = Depends(get_current_active_user)):
    """
    Gets all environments from the requester account.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Viewer", "Editor", "Admin"])
    # Try our db query.
    try:
        # Find our account.
        response = db.accounts.find_one({"account": current_user["account"]})
        # Log for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log error.
        logger.error(f"error: {e}")
        # Raise exception.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
    # Instantiate response data object with our returned account for validation.
    data = {"account": response["account"]}
    # If environments in our response add it.
    if "environments" in response:
        # Add our environments to the data object.
        data["environments"] = response["environments"]
    # Log for debugging.
    logger.debug(f"environment data: {data}")
    # Check our user for unintended data.
    validated_data = check_response(current_user, data)
    # Log our validated_response for debugging.
    logger.debug(f"validated_data: {validated_data}")
    # Return the validate_data to the client.
    return validated_data["environments"]


@router.post("/")
async def update_environment(
    environment: UpdateEnvironment,
    current_user: User = Depends(get_current_active_user),
):
    """
    Updates environment list.
    """
    # Verify the user has the allowed role.
    verify_role(current_user, ["Admin"])
    # We can't insert the model, so we have to convert to dict.
    environment_dict = environment.dict()
    # Log for debugging.
    logger.debug(f"environment_dict: {environment_dict}")

    # Try our db upsert.
    try:
        # Put the new environment list in the db.
        resp = db.accounts.update_one(
            {"account": current_user["account"]},
            {"$set": {"environments": environment_dict["environments"]}},
            upsert=True,
        )
        # Log for debugging.
        logger.debug(f"resp.matched_count: {resp.matched_count}")
        logger.debug(f"resp.modified_count: {resp.modified_count}")
        logger.debug(f"resp.upserted_id: {resp.upserted_id}")
    except Exception as e:
        # Log error.
        logger.error(f"Unexpected error occurred. {e}")
        # Raise exception.
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred. {e}")

    # Return success.
    return {"detail": "Environments updated successfully."}
