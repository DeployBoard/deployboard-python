import logging
import requests
from flask import Blueprint, render_template, session

users_page = Blueprint('users_page', __name__)
logger = logging.getLogger(__name__)


@users_page.route('/')
def users():
    """
    Queries our users api endpoint then passes that data into the users template
    """
    # Get data from our users api endpoint.
    try:
        response = requests.get(
            'http://api:8081/users',
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
    except Exception as e:
        return render_template("users.html", error=e)
    # Log our response for debugging.
    logger.debug(f"users response: {response.json()}")
    # Set our services variable that we will pass into the template.
    user_list = response.json()
    # Return our template.
    return render_template("users.html", users=user_list)
