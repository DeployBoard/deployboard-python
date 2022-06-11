import logging
import random
import string

import requests
from flask import Blueprint, redirect, render_template, request, session, url_for
from jose import jwt
from webutil.auth.session import set_session
from webutil.auth.sso import check_sso_provider
from webutil.config import config
from webutil.webapi import webapi

okta_page = Blueprint("okta_page", __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = config("APP_SECRET")
ALGORITHM = "HS256"

# Generate a random string for our Okta STATE value.
OKTA_STATE = "".join(random.choice(string.ascii_lowercase) for i in range(32))
# Generate a random string for our Okta NONCE value.
OKTA_NONCE = "".join(random.choice(string.ascii_lowercase) for i in range(32))


@okta_page.route("/", methods=["GET"])
def login_okta():
    # Create our get request params.
    query_params = {
        "client_id": config("OKTA_CLIENT_ID"),
        "redirect_uri": config("OKTA_REDIRECT_URL"),
        "scope": config("OKTA_SCOPES"),
        "state": OKTA_STATE,
        "nonce": OKTA_NONCE,
        "response_type": "code",
        "response_mode": "query",
    }

    # Build request_uri.
    request_uri = f"{config('OKTA_AUTH_URL')}?{requests.compat.urlencode(query_params)}"

    return redirect(request_uri)


@okta_page.route("/callback", methods=["GET"])
def login_okta_callback():
    # Upon successful login, Okta returns to this page with a "code".

    # Check if we are using sso, so we can add that login button to the template.
    sso = check_sso_provider()
    # Get the code from the query string params.
    code = request.args.get("code")
    # Log code for debugging.
    logger.debug(f"code: {code}")
    # If we don't have a code, return an error.
    if not code:
        if request.args.get("error") and request.args.get("error_description"):
            error_message = (
                f"{request.args.get('error')}: {request.args.get('error_description')}"
            )
            return render_template(
                "login.html", header=False, sso=sso, error=error_message
            )
        return "The code was not returned or is not accessible", 403

    # Send the code to the /token route to get a valid DPB token.
    data = {"okta_code": code}
    try:
        # Call our api endpoint.
        response = webapi("post", "token/", data=data, auth_method=sso["name"])
        # Log response for debugging.
        logger.debug(f"response: {response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("login.html", header=False, sso=sso, error=e)

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
        username="matt@deployboard.io",  # TODO: don't hardcode this....
        auth_method=sso["name"],
    )

    # Log session for debugging.
    logger.info(f"session: {session}")

    return redirect(url_for("dashboard_page.dashboard"))
