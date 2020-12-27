import os
import logging
import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

logs_page = Blueprint('logs_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']
ALGORITHM = "HS256"


# TODO: Add support for optional query string filters
@logs_page.route('/')
def logs():
    """
    Queries our logs api endpoint then passes that data into the logs template
    """
    # Get data from our deployments api endpoint.
    response = requests.get(
        'http://api:8081/logs',
        headers={'Authorization': f'Bearer {session["token"]}'}
    )
    # Log our response for debugging.
    logger.debug(f"logs response: {response.json()}")
    # Set our versions variable that we will pass into the template.
    logs_data = response.json()
    # Return our template.
    return render_template("logs.html", logs=logs_data)
