import logging

from flask import Blueprint, redirect, render_template, request, session, url_for
from webutil.webapi import webapi

me_page = Blueprint("me_page", __name__)
logger = logging.getLogger(__name__)


@me_page.route("/", methods=["GET"])
def me():
    """
    Queries our me api endpoint then passes that data into the me template
    """
    try:
        # Get data from our me api endpoint.
        response = webapi("get", "me/", token=session["token"])
        # Log for debugging
        logger.debug(f"me_response: {response}")
    except Exception as error:
        # Return our template with an error.
        return render_template("dashboard.html", error=error)
    # Return our template.
    return render_template("me.html", me=response)


@me_page.route("/", methods=["POST"])
def update_me():
    """
    Parses the request form and sends a patch request to our me api endpoint.
    """
    # TODO: Some of this should not work if we're using an SSO provider.
    # set our post data from request form.
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "avatar": request.form["avatar"],
        "theme": request.form["theme"],
    }
    try:
        # Send data to our me api endpoint.
        response = webapi("patch", "me/", token=session["token"], json=data)
        # Log for debugging
        logger.debug(f"me_response: {response}")
    except Exception as error:
        # Return our template with an error.
        return render_template("me.html", error=error)
    # Return our template.
    return redirect(url_for("me_page.me"))
