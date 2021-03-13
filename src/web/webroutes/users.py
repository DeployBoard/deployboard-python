import logging
from flask import Blueprint, render_template, session
from webutil.webapi import webapi

users_page = Blueprint('users_page', __name__)
logger = logging.getLogger(__name__)


@users_page.route('/')
def users():
    """
    Queries our users api endpoint then passes that data into the users template
    """
    try:
        # Call our api endpoint.
        response = webapi('get', 'users/', token=session['token'])
        # Log response for debugging.
        logger.debug(f'response: {response}')
    except Exception as e:
        # Log exception.
        logger.error(f'Exception: {e}')
        # Return our page with error.
        return render_template("users.html", error=e)
    # Return our template.
    return render_template("users.html", users=response)
