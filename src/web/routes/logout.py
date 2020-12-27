import logging
from flask import Blueprint, session, redirect, url_for

logout_page = Blueprint('logout_page', __name__)

logger = logging.getLogger(__name__)


@logout_page.route('/')
def logout():
    """
    Clears the user session and redirects to login page
    """
    # Clear the user's session.
    session.clear()
    # Redirect to login page
    return redirect(url_for('login_page.login'))
