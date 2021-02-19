import os
import logging
import requests
from flask import Blueprint, render_template, session

dashboard_page = Blueprint('dashboard_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']


@dashboard_page.route('/')
def dashboard():
    """
    Queries our deployments api endpoint then passes that data into the dashboard template
    """
    try:
        # Get data from our services api endpoint.
        services = get_api('services', session['token'])
        # Get data from our environments api endpoint.
        environments = get_api('environments', session['token'])
    except Exception as error:
        # Return our template with an error.
        return render_template("dashboard.html", error=error), 500

    # Return our template.
    return render_template("dashboard.html", services=services, environments=environments)


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
        logger.debug(f"deployments response: {response.json()}")
    except Exception as error:
        # Log error for debugging.
        logger.error(f"deployments error: {error}")
        # Re-raise the same error.
        raise

    return response.json()
