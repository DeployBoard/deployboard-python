import logging
from flask import Blueprint, render_template, request, session, redirect, url_for
from webutil.webapi import get_api

environments_page = Blueprint('environments_page', __name__)
logger = logging.getLogger(__name__)


@environments_page.route('/')
def environments():
    """
    Queries our environments api endpoint then passes that data into the environments template
    """
    try:
        # Get data from our environments api endpoint.
        response = get_api('environments', session['token'])
    except Exception as error:
        # Return our template with an error.
        return render_template("dashboard.html", error=error)

    # Return our template.
    return render_template("environments.html", environments=response)
