from requests import request
import logging
from webutil.config import config

logger = logging.getLogger(__name__)


def webapi(method, route, token=None, data=None, json=None):
    """
    Query api endpoint and return response.
    """
    headers = {'Authorization': f'Bearer {token}'} if token is not None else None
    try:
        response = request(
            method,
            f'{config("DPB_API_URI")}/{route}',
            headers=headers,
            json=json,
            data=data
        )
        # Log our response for debugging.
        logger.debug(f"api {method} {route} response: {response.status_code} {response.json()}")
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
