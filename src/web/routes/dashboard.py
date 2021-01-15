import os
import logging
import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

dashboard_page = Blueprint('dashboard_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']


@dashboard_page.route('/')
def dashboard():
    """
    Queries our deployments api endpoint then passes that data into the dashboard template
    """
    # Get data from our deployments api endpoint.
    response = requests.get(
        'http://api:8081/services',
        headers={'Authorization': f'Bearer {session["token"]}'}
    )
    # Log our response for debugging.
    logger.debug(f"deployments response: {response.json()}")
    # Set our services variable that we will pass into the template.
    services = response.json()
    # TODO: Sort the display of the environments by the accounts preferred order.
    # Return our template.
    return render_template("dashboard.html", services=services)
