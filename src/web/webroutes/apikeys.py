import os
import logging
import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

apikeys_page = Blueprint('apikeys_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']


@apikeys_page.route('/')
def apikeys():
    """
    Queries our apikeys api endpoint then passes that data into the apikeys template
    """
    # Get data from our users api endpoint.
    response = requests.get(
        'http://api:8081/apikeys',
        headers={'Authorization': f'Bearer {session["token"]}'}
    )
    # Log our response for debugging.
    logger.debug(f"apikeys response: {response.json()}")
    # Set our services variable that we will pass into the template.
    apikeys_list = response.json()
    # Return our template.
    return render_template("apikeys.html", apikeys=apikeys_list)
