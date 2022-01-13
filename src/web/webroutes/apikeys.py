import logging

from flask import Blueprint, redirect, render_template, request, session, url_for
from webutil.webapi import webapi

apikeys_page = Blueprint("apikeys_page", __name__)
logger = logging.getLogger(__name__)


@apikeys_page.route("/", methods=["GET"])
def apikeys():
    """
    Queries our apikeys api endpoint then passes that data into the apikeys template
    """
    try:
        # Call our api endpoint.
        response = webapi("get", "apikeys/", token=session["token"])
        # Log response for debugging.
        logger.debug(f"apikeys response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("apikeys/apikeys.html", error=e)
    # Return our template.
    return render_template("apikeys/apikeys.html", apikeys=response)


@apikeys_page.route("/<_id>", methods=["GET"])
def apikeys_get_single(_id):
    """
    Queries our apikeys api endpoint for specific key _id
    then passes that data into the apikeys template
    """
    try:
        # Call our api endpoint.
        response = webapi("get", f"apikeys/{_id}", token=session["token"])
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("apikeys/apikey.html", error=e)
    # Return our template.
    return render_template("apikeys/apikey.html", key=response)


@apikeys_page.route("/", methods=["POST"])
def apikeys_post():
    """
    Determines the action from the request form and calls the appropriate function.
    """
    # Log our form for debugging
    logger.debug(f"request.form: {request.form}")

    # Instantiate our optional parameters
    apikey_data = {}
    extras = ""

    if request.form["action"] == "add":
        method = "put"
        apikey_data = {
            "name": request.form["apikey_name"],
            "role": request.form["apikey_role"],
        }
    elif request.form["action"] == "edit":
        method = "patch"
        extras = request.form["apikey_id"]
        # Create our apikey_data from the request form.
        apikey_data = {
            "name": request.form["apikey_name"],
            "role": request.form["apikey_role"],
            "enabled": request.form["apikey_enabled"],
        }
    elif request.form["action"] == "delete":
        method = "delete"
        extras = request.form["apikey_id"]
    else:
        # Log a warning.
        logger.warning("We reached a case that should not have happened.")
        # Return our template with error message.
        return render_template(
            "apikeys/apikeys.html", error="Unexpected error occurred."
        )

    # Make our backend api call.
    try:
        # Call our api endpoint.
        response = webapi(
            method, f"apikeys/{extras}", token=session["token"], json=apikey_data
        )
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our error.
        return render_template("apikeys/apikeys.html", error=e)

    # Return our template.
    return redirect(url_for("apikeys_page.apikeys"))
