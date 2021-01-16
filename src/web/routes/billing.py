import os
import logging
import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

billing_page = Blueprint('billing_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']
ALGORITHM = "HS256"


# TODO: Implement this route
@billing_page.route('/')
def billing():
    """
    Displays our billing.
    """
    # Return our template.
    return render_template("billing.html")
