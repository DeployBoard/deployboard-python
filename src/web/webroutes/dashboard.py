import logging

from flask import Blueprint, render_template, session
from webutil.webapi import webapi

dashboard_page = Blueprint("dashboard_page", __name__)
logger = logging.getLogger(__name__)


@dashboard_page.route("/")
def dashboard():
    """
    Queries our services api endpoint then passes that data into the dashboard template
    """
    try:
        # Call our services api endpoint.
        services = webapi("get", "services/", token=session["token"])
        # Log response for debugging.
        logger.debug(f"services_response: {services}")
        # Call our environments api endpoint.
        environments = webapi("get", "environments/", token=session["token"])
        # Log response for debugging.
        logger.debug(f"environments_response: {environments}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("dashboard.html", error=e)

    # TODO: Sort the services['environments'] by environment order we receive from
    #  environments api call.

    # Return our template.
    return render_template("dashboard.html", services=services)
