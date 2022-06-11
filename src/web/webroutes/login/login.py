import logging

from flask import Blueprint, redirect, render_template, request, session, url_for
from jose import jwt
from webutil.auth.session import set_session
from webutil.auth.sso import check_sso_provider
from webutil.config import config
from webutil.webapi import webapi

login_page = Blueprint("login_page", __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = config("APP_SECRET")
ALGORITHM = "HS256"


@login_page.route("/", methods=["GET"])
def login():
    # Check if we are using sso, so we can add that login button to the template.
    sso = check_sso_provider()
    # Check if we're already logged in and send us to the dashboard.
    if "logged_in" in session:
        logger.debug("User logged_in so go to dashboard.")
        return redirect(url_for("dashboard_page.dashboard"))
    return render_template("login.html", header=False, sso=sso)


@login_page.route("/", methods=["POST"])
def login_post():
    logger.debug(f"request form: {request.form}")
    attempted_username = request.form["email"]
    data = {
        "username": attempted_username,
        "password": request.form["password"],
    }
    headers = {"login_method": "local"}
    try:
        # Call our api endpoint.
        response = webapi(
            "post", "token/", data=data, headers=headers, auth_method="Basic"
        )
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("login.html", header=False, error=e)

    # Set our token from the response.
    token = response["access_token"]
    # Log token for debugging.
    logger.debug(f"token: {token}")

    # Decode our jwt from response - this holds our user's information
    token_decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    logger.info(f"token_decoded: {token_decoded}")

    # Set session from our decoded token information.
    set_session(
        token=token,
        logged_in=True,
        user_id=token_decoded["sub"],
        exp=token_decoded["exp"],
        username=attempted_username,
        auth_method="local",
    )

    # Log session for debugging.
    logger.info(f"session: {session}")

    return redirect(url_for("dashboard_page.dashboard"))
