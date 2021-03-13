import logging
from flask import Blueprint, render_template, session
from webutil.webapi import webapi

apikeys_page = Blueprint('apikeys_page', __name__)
logger = logging.getLogger(__name__)


@apikeys_page.route('/')
def apikeys():
    """
    Queries our apikeys api endpoint then passes that data into the apikeys template
    """
    try:
        # Call our api endpoint.
        apikeys = webapi('get', 'apikeys/', token=session['token'])
        # Log response for debugging.
        logger.debug(f'apikeys response: {apikeys}')
    except Exception as e:
        # Log exception.
        logger.error(f'Exception: {e}')
        # Return our page with error.
        return render_template("apikeys.html", error=e)
    # Return our template.
    return render_template("apikeys.html", apikeys=apikeys)
