import logging
import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

logs_page = Blueprint('logs_page', __name__)
logger = logging.getLogger(__name__)


@logs_page.route('/', methods=['GET'])
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
    # Get data from our logs api endpoint.
    logs_response = get_logs(query_string, session['token'])
    # Log our response for debugging.
    logger.debug(f"logs response: {logs_response}")
    # Set our versions variable that we will pass into the template.
    logs_data = logs_response

    # Get data from our services api endpoint for search options.
    services_response = get_services(session['token'])
    # Log our response for debugging.
    logger.debug(f"services response: {services_response}")
    # Set our versions variable that we will pass into the template.
    services_data = services_response
    # Instantiate our empty lists.
    applications = []
    services = []
    environments = []
    # Loop through our logs_data and pluck out our wanted key values.
    for service_dict in services_data:
        applications.append(service_dict['application'])
        services.append(service_dict['service'])
        for version in service_dict['versions']:
            environments.append(version['environment'])

    # Return our template.
    return render_template("logs.html",
                           logs=logs_data,
                           applications=set(applications),
                           services=set(services),
                           environments=set(environments),
                           query_string=query_string_dict)


@logs_page.route('/', methods=['POST'])
def logs_search():
    """
    Redirects back to the logs page, but appending the query string parameters from the form
    """
    # Log our form for debugging
    logger.debug(f'request.form: {request.form}')
    # Instantiate an empty dict that we will unpack for query params.
    query_params = {}
    # TODO: What if someone has an app/service/env actually named 'All'?... Probably won't happen.
    # Set our query string parameters if not our default value.
    if request.form['application'] != 'All':
        query_params['application'] = request.form['application']
    if request.form['service'] != 'All':
        query_params['service'] = request.form['service']
    if request.form['environment'] != 'All':
        query_params['environment'] = request.form['environment']
    # Return the logs page with our query string parameters from request form.
    return redirect(url_for('logs_page.logs', **query_params))


def get_logs(query_string, token):
    try:
        response = requests.get(
            f'http://api:8081/logs/?{query_string}',
            headers={'Authorization': f'Bearer {token}'}
        )
        # Log our response for debugging.
        logger.debug(f"response: {response.json()}")
    except Exception as error:
        # Log error for debugging.
        logger.error(f"error: {error}")
        # Re-raise the same error.
        raise

    return response.json()


def get_services(token):
    try:
        response = requests.get(
            f'http://api:8081/services/',
            headers={'Authorization': f'Bearer {token}'}
        )
        # Log our response for debugging.
        logger.debug(f"response: {response.json()}")
    except Exception as error:
        # Log error for debugging.
        logger.error(f"error: {error}")
        # Re-raise the same error.
        raise

    return response.json()
