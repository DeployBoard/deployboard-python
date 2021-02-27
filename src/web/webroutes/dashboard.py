import logging
from flask import Blueprint, render_template, session
from webutil.webapi import get_api

dashboard_page = Blueprint('dashboard_page', __name__)
logger = logging.getLogger(__name__)


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
