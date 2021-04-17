import logging

from flask import Blueprint, redirect, render_template, request, session, url_for
from webutil.webapi import webapi

applications_page = Blueprint("applications_page", __name__)
logger = logging.getLogger(__name__)


@applications_page.route("/", methods=["GET"])
def applications():
    """
    Queries our services api endpoint
    then passes that data into the applications template
    """
    try:
        # Call our api endpoint.
        response = webapi("get", "services/", token=session["token"])
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("applications.html", error=e)
    # Log our response for debugging.
    logger.debug(f"services response: {response}")
    # Instantiate our app_list
    app_list = []
    # Sort get unique applications from our services response.
    for service in response:
        app = service["application"]
        logger.debug(f"app: {app}")
        if app not in app_list:
            logger.debug(f"app_list: {app_list}")
            app_list.append(app)
    logger.debug(f"app_list: {app_list}")
    # Return our template.
    return render_template("applications.html", app_list=app_list, services=response)


@applications_page.route("/", methods=["POST"])
def add_application():
    """
    Creates a new top level application from our request form
    """
    # Log our form for debugging
    logger.debug(f"request.form: {request.form}")
    # Set data from our request form
    data = {
        "application": request.form["application_name"],
        "service": request.form["service_name"],
    }
    # Log our data for debugging
    logger.debug(f"data: {data}")
    try:
        # Call our api endpoint.
        response = webapi("put", "services/", token=session["token"], json=data)
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("applications.html", error=e)
    return redirect(url_for("applications_page.applications"))
