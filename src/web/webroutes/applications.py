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
    response = get_services(session['token'])
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


# TODO: Get this to work
@applications_page.route('/', methods=['POST'])
def add_application():
    """
    Creates a new top level application from our request form
    """
    # Log our form for debugging
    logger.debug(f'request.form: {request.form}')
    # Set application_name from our request form
    application_name = request.form['application_name']
    # Log our application name for debugging
    logger.debug(f'application_name: {application_name}')
    # Get data from our services api endpoint.
    # TODO: This needs to be a post, but is not ready yet.
    response = get_services(session['token'])
    # Log our response for debugging.
    logger.debug(f"services response: {response}")
    # Set our versions variable that we will pass into the template.
    services = response
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


def get_services(token):
    try:
        response = requests.get(
            f'http://api:8081/services/',
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
