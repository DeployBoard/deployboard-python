import logging

from flask import Blueprint, redirect, render_template, request, session, url_for
from webutil.webapi import webapi

users_page = Blueprint("users_page", __name__)
logger = logging.getLogger(__name__)


@users_page.route("/", methods=["GET"])
def users():
    """
    Queries our users api endpoint then passes that data into the users template
    """
    try:
        # Call our api endpoint.
        response = webapi("get", "users/", token=session["token"])
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("users/users.html", error=e)
    # Return our template.
    return render_template("users/users.html", users=response)


@users_page.route("/<_id>", methods=["GET"])
def users_get_single(_id):
    """
    Queries our users api endpoint for specific user _id
    then passes that data into the users template
    """
    # TODO: Implement this
    try:
        # Call our api endpoint.
        response = webapi("get", f"users/{_id}", token=session["token"])
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("users/user.html", error=e)
    # Return our template.
    return render_template("users/user.html", user=response)


@users_page.route("/", methods=["POST"])
def users_post():
    """
    Determines the action from the request form and calls the appropriate function.
    """
    # Log our form for debugging
    logger.debug(f"request.form: {request.form}")

    # Instantiate our optional parameters
    user_data = {}
    extras = ""

    if request.form["action"] == "add":
        method = "put"
        user_data = {
            "email": request.form["user_email"],
            "role": request.form["user_role"],
            "first_name": request.form["user_first_name"],
            "last_name": request.form["user_last_name"],
            "password": request.form["user_password"],
        }
    elif request.form["action"] == "edit":
        method = "patch"
        extras = request.form["user_id"]
        # Create our user_data from the request form, omitting password.
        user_data = {
            "email": request.form["user_email"],
            "role": request.form["user_role"],
            "enabled": request.form["user_enabled"],
            "first_name": request.form["user_first_name"],
            "last_name": request.form["user_last_name"],
        }
        # If password is empty we want to leave it out of the user_data.
        if request.form["user_password"] != "":
            user_data["password"] = request.form["user_password"]
    elif request.form["action"] == "delete":
        method = "delete"
        extras = request.form["user_id"]
    else:
        # Log a warning.
        logger.warning("We reached a case that should not have happened.")
        # Return our template with error message.
        return render_template("users/users.html", error="Unexpected error occurred.")

    # Make our backend api call.
    try:
        # Call our api endpoint.
        response = webapi(
            method, f"users/{extras}", token=session["token"], json=user_data
        )
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our error.
        return render_template("users/users.html", error=e)

    # Return our template.
    return redirect(url_for("users_page.users"))
