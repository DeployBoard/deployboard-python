import logging

from flask import Blueprint, redirect, render_template, request, session, url_for
from webutil.webapi import webapi

logs_page = Blueprint("logs_page", __name__)
logger = logging.getLogger(__name__)


@logs_page.route("/", methods=["GET"])
def logs():
    """
    Queries our logs api endpoint then passes that data into the logs template
    """
    # Get our query string to forward into the api call for filtering.
    query_string = request.query_string.decode()
    # Log our query string for debugging.
    logger.debug(f"query_string: {query_string}")
    # Convert our query string to dict to pass into our template.
    query_string_dict = request.args.to_dict()
    # Log our query string dict for debugging.
    logger.debug(f"query_string_dict: {query_string_dict}")
    try:
        # Call our logs api endpoint.
        logs_response = webapi("get", f"logs/?{query_string}", token=session["token"])
        # Log response for debugging.
        logger.debug(f"logs_response: {logs_response}")
        # Call our services api endpoint.
        services_response = webapi("get", "services/", token=session["token"])
        # Log response for debugging.
        logger.debug(f"services_response: {services_response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return our page with error.
        return render_template("logs.html", error=e)

    # Instantiate our empty lists.
    applications = []
    services = []
    environments = []
    # Loop through our services_response and pluck out our wanted key values.
    for service_dict in services_response:
        applications.append(service_dict["application"])
        services.append(service_dict["service"])
        # We could get the environment list from the environments api endpoint,
        #  but we are already looping through the services,
        #  so just get environments from here.
        for environment in service_dict["environments"]:
            environments.append(environment)

    # Log our lists for debugging.
    logger.debug(f"applications_list: {applications}")
    logger.debug(f"services_list: {services}")
    logger.debug(f"environments_list: {environments}")

    # Return our template. Converting our lists to sets to remove duplicate values.
    return render_template(
        "logs.html",
        logs=logs_response,
        applications=set(applications),
        services=set(services),
        environments=set(environments),
        query_string=query_string_dict,
    )


@logs_page.route("/", methods=["POST"])
def logs_search():
    """
    Redirects back to the logs page,
    but appending the query string parameters from the form
    """
    # Log our form for debugging
    logger.debug(f"request.form: {request.form}")
    # Instantiate an empty dict that we will unpack for query params.
    query_params = {}
    # TODO: What if someone has an app/service/env actually named 'All'?...
    #  Probably won't happen.
    # Set our query string parameters if not our default value.
    if request.form["application"] != "All":
        query_params["application"] = request.form["application"]
    if request.form["service"] != "All":
        query_params["service"] = request.form["service"]
    if request.form["environment"] != "All":
        query_params["environment"] = request.form["environment"]
    # Return the logs page with our query string parameters from request form.
    return redirect(url_for("logs_page.logs", **query_params))
