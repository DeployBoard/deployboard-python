import os
import logging
import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

applications_page = Blueprint('applications_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']
ALGORITHM = "HS256"


@applications_page.route('/', methods=['GET'])
def applications():
    """
    Queries our services api endpoint then passes that data into the applications template
    """
    # Get data from our services api endpoint.
    response = requests.get(
        'http://api:8081/services',
        headers={'Authorization': f'Bearer {session["token"]}'}
    )
    # Log our response for debugging.
    logger.debug(f"services response: {response.json()}")
    # Set our versions variable that we will pass into the template.
    services = response.json()
    # Instantiate our app_list
    app_list = []
    # Sort get unique applications from our services.
    for service in services:
        app = service['application']
        logger.debug(f"app: {app}")
        if app not in app_list:
            logger.debug(f"app_list: {app_list}")
            app_list.append(app)
    logger.debug(f"app_list: {app_list}")
    # Return our template.
    return render_template("applications.html", app_list=app_list, services=services)


@applications_page.route('/', methods=['POST'])
def add_application():
    """
    Queries our services api endpoint then passes that data into the applications template
    """
    logger.debug(f'request.form: {request.form}')
    application_name = request.form['application_name']
    logger.debug(f'application_name: {application_name}')
    # Get data from our services api endpoint.
    response = requests.get(
        'http://api:8081/services',
        headers={'Authorization': f'Bearer {session["token"]}'}
    )
    # Log our response for debugging.
    logger.debug(f"services response: {response.json()}")
    # Set our versions variable that we will pass into the template.
    services = response.json()
    # Instantiate our app_list
    app_list = []
    # Sort get unique applications from our services.
    for service in services:
        app = service['application']
        logger.debug(f"app: {app}")
        if app not in app_list:
            logger.debug(f"app_list: {app_list}")
            app_list.append(app)
    logger.debug(f"app_list: {app_list}")
    # Return our template.
    return render_template("applications.html", app_list=app_list, services=services)
