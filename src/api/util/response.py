import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def check_response(current_user, response):
    """
    Checks our response for any security issues.
    """
    # TODO: Recursively check all keys anywhere in the response. Currently this only checks top level keys.
    # TODO: Move this to a middleware that catches all outgoing responses, and doesn't rely on the method to
    #  call it explicitly.
    # Check if the response data contains items from account different than our requester.
    if current_user['account'] != response['account']:
        # Log for debugging
        logger.error(f"accounts do not match: {current_user['account']} != {response['account']}")
        # Raise exception
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
    # Check if the response data contains hashed_password.
    if 'hashed_password' in response:
        # Log for debugging
        logger.error(f"hashed_password found in response: {response}")
        # Raise exception
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
    # If all of our checks pass, return the response
    return response
