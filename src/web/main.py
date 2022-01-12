import logging
from datetime import datetime

from flask import Flask, redirect, request, session, url_for
from flask_wtf.csrf import CSRFProtect
from webroutes.analytics import analytics_page
from webroutes.apikeys import apikeys_page
from webroutes.applications import applications_page
from webroutes.billing import billing_page
from webroutes.ci import ci_page
from webroutes.dashboard import dashboard_page
from webroutes.environments import environments_page
from webroutes.integrations import integrations_page
from webroutes.login import login_page
from webroutes.logout import logout_page
from webroutes.logs import logs_page
from webroutes.me import me_page
from webroutes.users import users_page
from webroutes.versions import versions_page
from webutil.config import config
from webutil.webapi import webapi

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = config("APP_SECRET")
csrf = CSRFProtect(app)

app.register_blueprint(login_page, url_prefix="/login")
app.register_blueprint(logout_page, url_prefix="/logout")
app.register_blueprint(dashboard_page, url_prefix="/dashboard")
app.register_blueprint(versions_page, url_prefix="/dashboard/versions")
app.register_blueprint(ci_page, url_prefix="/ci")
app.register_blueprint(applications_page, url_prefix="/applications")
app.register_blueprint(logs_page, url_prefix="/logs")
app.register_blueprint(analytics_page, url_prefix="/analytics")
app.register_blueprint(me_page, url_prefix="/me")
app.register_blueprint(users_page, url_prefix="/settings/users")
app.register_blueprint(apikeys_page, url_prefix="/settings/apikeys")
app.register_blueprint(integrations_page, url_prefix="/settings/integrations")
app.register_blueprint(billing_page, url_prefix="/settings/billing")
app.register_blueprint(environments_page, url_prefix="/settings/environments")


@app.route("/")
def index():
    # If user is logged in.
    if "logged_in" in session:
        # We're logged in so go to dashboard.
        return redirect(url_for("dashboard_page.dashboard"))
    # We're not logged in so app.before_request will send us to login page.


@app.before_request
def check_session_expired():
    """Checks if session is expired"""
    # If user is logged in.
    if "logged_in" in session:
        # Check if we have exp in session.
        if "exp" in session:
            # If session is not expired.
            # TODO: Remove this when refresh token is in place
            if session["exp"] < datetime.now().timestamp():
                # Clear the user's session.
                session.clear()
                # redirect to login page to clear session,
                # which will redirect to login page.
                return redirect(url_for("logout_page.logout"))
    elif "login" in request.base_url:
        # Ignore if /login
        pass
    elif "static" in request.base_url:
        # Ignore if /static/*
        pass
    else:
        # Redirect all unauthenticated requests to the login page.
        return redirect(url_for("login_page.login"))


@app.before_request
def get_me_info():
    """
    Queries our me api endpoint then passes that data into the me template
    """
    try:
        # Get data from our me api endpoint.
        response = webapi("get", "me/", session["token"])
        # Set session from response.
        session["theme"] = response["theme"]
        # Set account from response.
        session["account"] = response["account"]
    except Exception as error:
        # Log error.
        logger.error(f"me error: {error}")
        # For now we just pass on without doing anything.
        # We'll let the destination route throw error if that endpoint
        # is unable to load. This may change in the future.


@app.template_filter()
def epoch_to_date(epoch):
    """Converts epoch to timezone in user's profile"""
    # TODO: Get timezone from the user's session, and convert to that.
    #  Need to first set it in user's session after login.
    # Log for debugging.
    logger.debug(f"epoch: {epoch}")
    # Set date from epoch.
    new_date = datetime.fromtimestamp(epoch)
    # Format the date.
    formatted_date = new_date.strftime("%m/%d/%Y %H:%M:%S")
    # Return the formatted date.
    return formatted_date


@app.context_processor
def inject_theme():
    """Injects globals into Jinja templates"""
    # Check if theme is in session.
    if "theme" in session:
        # If theme in session, use the theme.
        theme = session["theme"]
    else:
        theme = "light"
    return dict(theme=theme)


@app.route("/settings", methods=["GET"], strict_slashes=False)
def settings():
    return redirect(url_for("users_page.users"))


if __name__ == "__main__":
    app.run(
        host=config("DPB_WEB_HOST"),
        port=config("DPB_WEB_PORT"),
        debug=config("DPB_WEB_DEBUG"),
    )
