import os
import logging
import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

ci_page = Blueprint('ci_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']
ALGORITHM = "HS256"


# TODO: Implement this route - https://github.com/DeployBoard/deployboard/issues/5
@ci_page.route('/')
def ci():
    """
    Displays our temporary environments.
    """
    # Return our template.
    return render_template("ci.html")
