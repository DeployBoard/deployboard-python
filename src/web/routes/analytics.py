import os
import logging
import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

analytics_page = Blueprint('analytics_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']
ALGORITHM = "HS256"


@analytics_page.route('/', methods=['GET'])
def analytics():
    """
    Analytics
    """
    # Return our template.
    return render_template("analytics.html")
