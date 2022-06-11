import logging

from flask import Blueprint, redirect, session, url_for

logout_page = Blueprint("logout_page", __name__)
logger = logging.getLogger(__name__)


@logout_page.route("/")
def logout():
    """
    Clears the user session and redirects to login page
    """
    # Log user's session before clearing.
    logger.debug(f"session after clear: {session}")
    # Clear the user's session.
    session.clear()
    # Log user's session after clearing.
    logger.debug(f"session after clear: {session}")
    # Redirect to login page
    return redirect(url_for("login_page.login"))
