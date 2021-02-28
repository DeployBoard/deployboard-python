import requests
import logging

logger = logging.getLogger(__name__)


def get_api(route, token):
    """
    Query api endpoint and return response.
    """
    try:
        response = requests.get(
            f'http://api:8081/{route}',
            headers={'Authorization': f'Bearer {token}'}
        )
        # Log our response for debugging.
        logger.debug(f"api response: {response.json()}")
    except Exception as error:
        # Log error for debugging.
        logger.error(f"api error: {error}")
        # Re-raise the same error.
        raise
    return response.json()


def post_api(route, token, data):
    """
    Post to api endpoint and return response.
    """
    try:
        response = requests.post(
            f'http://api:8081/{route}',
            headers={'Authorization': f'Bearer {token}'},
            json=data
        )
        # Log our response for debugging.
        logger.debug(f"deployments response: {response.json()}")
    except Exception as error:
        # Log error for debugging.
        logger.error(f"deployments error: {error}")
        # Re-raise the same error.
        raise
    return response.json()
