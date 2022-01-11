import logging
from datetime import datetime

from db.mongo import db
from fastapi import APIRouter, Depends, HTTPException
from models.deployments import DeploymentRequest
from models.logs import Log
from util.auth import get_api_key_in_header, verify_api_key, verify_role
from util.hash import hash_dict, hash_string

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/deploy", tags=["Deploy"], responses={404: {"description": "Not found"}}
)


# This endpoint is protected by API key, not by JWT.
@router.api_route("/", methods=["PUT", "POST"])
async def create_or_update_deployment(
    body: DeploymentRequest, api_key: str = Depends(get_api_key_in_header)
):
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
    deployment["timestamp"] = datetime.utcnow().timestamp()
    # Add the account from our api key.
    deployment["account"] = api_key_object["account"]

    # Create environment if it does not exist in our account.
    handle_environment(deployment["account"], deployment["environment"])

    # Generate the hashed value for our new deployment object.
    deployment["hash"] = hash_dict(deployment)

    # Get previous log's hash.
    previous_hash = get_previous_log_hash(
        deployment["account"],
        deployment["application"],
        deployment["service"],
        deployment["environment"],
    )

    # Hash the two hashes together to generate our hash_chain value.
    deployment["hash_chain"] = hash_string(deployment["hash"] + previous_hash)

    # Insert our object, including our new hashes, into the logs db.
    insert_to_logs(deployment)

    # Update the service that matches our account+application.
    update_service_with_latest(deployment)

    return {"status": "ok"}


def handle_environment(account, environment):
    """
    Adds the passed environment to the environment list in the accounts collection.
    """

    # Set our query for the update.
    query = {"account": account}
    # Create our update command to add the environment.
    # addToSet is used to append to the array, only if it is not already in the array.
    update_command = {"$addToSet": {"environments": environment}}

    try:
        # Update the environments list in the accounts collection.
        result = db.accounts.update_one(query, update_command)
        # Log the result for debugging.
        logger.debug(f"update_account_environment_result: {result.raw_result}")
    except Exception as e:
        # Log exception.
        logger.error(f"exception: {e}")
        # Raise exception.
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {e}")

    if result.matched_count == 0:
        # Log exception.
        logger.critical("handle_environment: No matching account, please report issue.")
        # Raise exception.
        raise HTTPException(
            status_code=500,
            detail=(
                f"Unexpected error occurred: No account found {result.matched_count}."
            ),
        )

    return


def get_previous_log_hash(account, application, service, environment):
    """
    Gets most recent log matching the account+app+service+env combination
    and returns the hash_chain.
    """

    logger.debug("Attempting to get_previous_log_hash")

    try:
        # Find the most recent log matching the account+app+service+env combination.
        result = list(
            db.logs.find(
                {
                    "account": account,
                    "application": application,
                    "service": service,
                    "environment": environment,
                }
            )
            .sort("timestamp", -1)
            .limit(1)
        )

        # If an object already exists, we want to just take that hash,
        # else we want to return an empty string.
        if len(result) > 0:
            # Log for debugging.
            logger.debug(f"get_previous_log_hash_result: {result}")
            # Return result.
            return result[0]["hash_chain"]
        else:
            # Log for debugging.
            logger.debug("get_previous_log_hash_result: None")
            # Return empty string.
            return ""

    except Exception as e:
        # Log exception.
        logger.error(f"get_previous_log_hash_exception: {e}")
        # Raise exception.
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {e}")


def insert_to_logs(deployment: Log):
    """
    Insert into the logs collection.
    """
    logger.debug("Attempting: insert_to_logs")
    try:
        # Insert the deployment object into the logs db.
        result = db.logs.insert_one(deployment)
        # Log the inserted id for debugging.
        logger.debug(f"insert_logs_result: {result.inserted_id}")
    except Exception as e:
        # Log exception.
        logger.error(f"exception: {e}")
        # Raise exception.
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {e}")

    return


def update_service_with_latest(deployment):
    """
    Update the service in the services collection with the latest data.
    """

    service_response = find_service(
        deployment["account"], deployment["application"], deployment["service"]
    )

    if service_response is None:
        # Create entirely new service.
        create_new_service(deployment)
    else:
        # Service already exists, so update the environment.
        update_existing_service(deployment)

    return


def find_service(account, application, service):
    """
    Find the service in the database, if it exists.
    """

    # Set our query.
    query = {"account": account, "application": application, "service": service}

    try:
        # Find our service.
        result = list(db.services.find(query))
        # Log the result for debugging.
        logger.debug(f"find_service_count: {len(result)}")
    except Exception as e:
        # Log our exception for debugging.
        logger.error(f"e: {e}")
        # Raise exception if failed to insert.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    # If the service does not exist, we want to return None, else return the result.
    if len(result) == 0:
        # Log for debugging.
        logger.debug("find_service_result: None")
        # Return None.
        return None
    if len(result) > 1:
        # Log exception.
        logger.critical(
            "find_service_error: "
            "more than 1 service returned. Please report this issue."
        )
        # Raise exception.
        raise HTTPException(
            status_code=500,
            detail=(
                f"Unexpected error occurred: Multiple services found {len(result)}."
            ),
        )
    else:
        # Log for debugging.
        logger.debug(f"find_service_result: {result[0]}")
        # Return result.
        return result[0]


def create_new_service(deployment):
    """
    Create new service, inserting our deployment data.
    """

    # TODO: Can we use the service pydantic model here
    #  to make sure we're always in sync?
    # Build our service object to insert
    service = {
        "schema_version": 1.0,
        "account": deployment["account"],
        "application": deployment["application"],
        "service": deployment["service"],
        "tags": [],
        "environments": {
            deployment["environment"]: {
                "version": deployment["version"],
                "status": deployment["status"],
                "timestamp": deployment["timestamp"],
                "custom": deployment["custom"],
            }
        },
    }
    # Log for debugging
    logger.debug(f"create_new_service:service: {service}")

    try:
        # Insert new service into the services collection
        response = db.services.insert_one(service)
        # Log
        logger.info(f"insert_service_response: {response.inserted_id}")
    except Exception as e:
        # Log our exception for debugging.
        logger.error(f"e: {e}")
        # Raise exception if failed to insert.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    return response.inserted_id


def update_existing_service(deployment):
    """
    Update existing service with new environment.
    """

    # Set our query for the update.
    query = {
        "account": deployment["account"],
        "application": deployment["application"],
        "service": deployment["service"],
    }
    # Create our update command to add the environment.
    # addToSet is used to append to the array, only if it is not already in the array.
    update_command = {
        "$set": {
            "environments": {
                deployment["environment"]: {
                    "version": deployment["version"],
                    "status": deployment["status"],
                    "timestamp": deployment["timestamp"],
                    "custom": deployment["custom"],
                }
            }
        }
    }

    try:
        # Update our service.
        response = db.services.update_one(query, update_command)
        # Log the result for debugging.
        logger.debug(f"insert_logs_result: {response.raw_result}")
    except Exception as e:
        # Log our exception for debugging.
        logger.error(f"e: {e}")
        # Raise exception if failed to insert.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    # If we failed to modify existing item, raise exception.
    if response.modified_count == 1:
        # Log for debugging.
        logger.debug("find_service_result: None")
        # Return True.
        return response.modified_count
    else:
        # Log exception.
        logger.critical(
            "update_existing_service: No matching service found."
            "Please report this issue."
        )
        # Raise exception.
        raise HTTPException(
            status_code=500,
            detail=(
                "Unexpected error occurred: "
                f"No matching service found {response.modified_count}."
            ),
        )
