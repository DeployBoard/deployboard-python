import logging

from flask import Blueprint, redirect, render_template, request, session, url_for
from webutil.webapi import webapi

environments_page = Blueprint("environments_page", __name__)
logger = logging.getLogger(__name__)


@environments_page.route("/")
def environments():
    """
    Queries our environments api endpoint then passes that data into the template
    """
    try:
        # Call our api endpoint.
        response = webapi("get", "environments/", token=session["token"])
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("environments.html", error=e)
    # Return our template.
    return render_template("environments.html", environments=response)


@environments_page.route("/", methods=["POST"])
def environments_post():
    """
    Determines the action from the request form and calls the appropriate function.
    """
    # Log our form for debugging
    logger.debug(f"request.form: {request.form}")

    # Instantiate our optional parameters
    environment_data = {}

    if request.form["action"] == "up":
        # The list comes in as a string in the request form. Convert string to list.
        environment_list = (
            request.form["environment_list"].strip("]'[").replace("'", "").split(", ")
        )
        # Get current position.
        old_index = environment_list.index(request.form["environment_name"])
        # If the old index is already 0, we don't want to do anything.
        if old_index == 0:
            # Log for debugging.
            logger.debug("Already at the 0 index, can't move up anymore.")
            # Return our template with warning message.
            return render_template(
                "environments.html",
                error=f"{request.form['environment_name']} is already top priority.",
            )
        # Moving up means we need to subtract the position in the list.
        new_index = old_index - 1
        # Pop out the old index, and insert the popped environment into the new index.
        environment_list.insert(new_index, environment_list.pop(old_index))
        # Set our method and data.
        method = "post"
        environment_data = {"environments": environment_list}
    elif request.form["action"] == "down":
        # The list comes in as a string in the request form. Convert string to list.
        environment_list = (
            request.form["environment_list"].strip("]'[").replace("'", "").split(", ")
        )
        # Get current position.
        old_index = environment_list.index(request.form["environment_name"])
        # If the old index is already end of the list, we don't want to do anything.
        if old_index == len(environment_list) - 1:
            # Log for debugging.
            logger.debug("Already at the last index, can't move down anymore.")
            # Return our template with warning message.
            return render_template(
                "environments.html",
                error=f"{request.form['environment_name']} is already lowest priority.",
            )

        # Moving up means we need to add the position in the list.
        new_index = old_index + 1
        # Pop out the old index, and insert the popped environment into the new index.
        environment_list.insert(new_index, environment_list.pop(old_index))
        # Set our method and data.
        method = "post"
        environment_data = {"environments": environment_list}
    else:
        # Log a warning.
        logger.warning("We reached a case that should not have happened.")
        # Return our template with error message.
        return render_template("environments.html", error="Unexpected error occurred.")

    # Make our backend api call.
    try:
        # Call our api endpoint.
        response = webapi(
            method,
            "environments/",
            token=session["token"],
            json=environment_data,
        )
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our error.
        return render_template("environments.html", error=e)

    # Return our template.
    return redirect(url_for("environments_page.environments"))
