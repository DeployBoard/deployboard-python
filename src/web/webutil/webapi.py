import logging

from requests import request
from webutil.config import config

logger = logging.getLogger(__name__)


def webapi(
    method,
    route,
    headers=None,
    token=None,
    data=None,
    json=None,
    auth_method=None,
):
    """
    Query api endpoint and return response.
    """
    # Init our headers if none were passed.
    if headers is None:
        headers = {}

    if token:
        # Set Authorization header as Bearer if we have a token.
        headers["Authorization"] = f"Bearer {token}"

    # auth_method is only used during the /token route.
    if auth_method:
        # Set Authorization header to auth_method if we pass it.
        headers["Authorization"] = auth_method

    # Content-Type to our api is always "application/json"
    headers["Content-Type"] = "application/json"

    logger.debug(f"headers: {headers}")
    try:
        response = request(
            method,
            f'{config("DPB_API_URI")}/{route}',
            headers=headers,
            json=json,
            data=data,
        )
        # Log our response for debugging.
        logger.debug(
            f"api {method} {route} response: {response.status_code} {response.json()}"
        )
    except Exception as error:
        # Log error for debugging.
        logger.error(f"api {method} {route} error: {error}")
        # Re-raise the same error.
        raise

    # If the api returns anything other than a 200
    #  raise that as an exception so the route can do something with it.
    if response.status_code != 200:
        raise Exception(response.status_code, response.json())

    return response.json()
