import logging
from flask import Blueprint, render_template, session
from webutil.webapi import webapi

environments_page = Blueprint('environments_page', __name__)
logger = logging.getLogger(__name__)


@environments_page.route('/')
def environments():
    """
    Queries our environments api endpoint then passes that data into the environments template
    """
    try:
        # Call our api endpoint.
        response = webapi('get', 'environments/', token=session['token'])
        # Log response for debugging.
        logger.debug(f'response: {response}')
    except Exception as e:
        # Log exception.
        logger.error(f'Exception: {e}')
        # Return our page with error.
        return render_template("environments.html", error=e)
    # Return our template.
    return render_template("environments.html", environments=response)
