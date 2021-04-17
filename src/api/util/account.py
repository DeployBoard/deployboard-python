import logging

from db.mongo import db
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def get_account(account):
    """
    Gets the account.
    """
    try:
        # Find our account.
        response = db.accounts.find_one({"account": account})
        # Log for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log error.
        logger.error(f"error: {e}")
        # Raise exception.
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {e}.")
    # Verify we found an account.
    if response is None:
        raise HTTPException(status_code=400, detail="Account not found.")
    # Return our response
    return response
