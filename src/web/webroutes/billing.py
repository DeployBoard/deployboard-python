import logging

from flask import Blueprint, render_template

billing_page = Blueprint("billing_page", __name__)
logger = logging.getLogger(__name__)


# TODO: Implement this route
@billing_page.route("/")
def billing():
    """
    Displays our billing.
    """
    # Return our template.
    return render_template("billing.html")
