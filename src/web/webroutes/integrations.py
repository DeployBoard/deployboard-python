import logging
from flask import Blueprint, render_template, request, session, redirect, url_for

integrations_page = Blueprint('integrations_page', __name__)
logger = logging.getLogger(__name__)


# TODO: Implement this route
@integrations_page.route('/')
def integrations():
    """
    Displays our integrations.
    """
    # Return our template.
    return render_template("integrations.html")
