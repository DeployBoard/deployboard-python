import os
import logging
import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

environments_page = Blueprint('environments_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']


@environments_page.route('/')
def environments():
    """
    Queries our environments api endpoint then passes that data into the environments template
    """
    # Get data from our users api endpoint.
    response = requests.get(
        'http://api:8081/environments',
        headers={'Authorization': f'Bearer {session["token"]}'}
    )
    # Log our response for debugging.
    logger.debug(f"environments response: {response.json()}")
    # Set our services variable that we will pass into the template.
    environments_list = response.json()
    # Return our template.
    return render_template("environments.html", environments=environments_list)
