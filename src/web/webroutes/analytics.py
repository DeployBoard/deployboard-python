import os
import logging
import requests
from datetime import datetime, timedelta
from dateutil import tz
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
    # Get our query string to forward into the api call for filtering.
    query_string = request.query_string.decode()
    # Log our query string for debugging.
    logger.debug(f"query_string: {query_string}")
    # Convert our query string to dict to pass into our template.
    query_string_dict = request.args.to_dict()


    # We need to convert our daysago from the query string to a from_timestamp for the logs api route.
    if 'daysago' in query_string_dict:
        # Generate date object of today at beginning of day (00:00:00) UTC.
        today = datetime.utcnow().date()
        # Get the start of today.
        start_of_today = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
        # Log for debugging.
        logger.debug(f'start_of_today: {start_of_today}')
        # subtract daysago from our start_of_today to get the start_of_days_ago.
        start_of_days_ago_epoch = datetime.timestamp(start_of_today - timedelta(int(query_string_dict['daysago'])))
        # Log for debugging.
        logger.debug(f'start_of_days_ago_epoch: {start_of_days_ago_epoch}')
        # Add from_timestamp to our query string as an int.
        query_string_dict['from_timestamp'] = int(start_of_days_ago_epoch)



    # Log our query string dict for debugging.
    logger.debug(f"query_string_dict: {query_string_dict}")
    # Get data from our logs api endpoint.
    logs_response = get_logs(query_string, session['token'])
    # Log our response for debugging.
    logger.debug(f"logs response: {logs_response}")
    # Set our versions variable that we will pass into the template.
    logs_data = logs_response


    # Generate our daily_deploy_data dict for the graph.
    daily_deploy_data = []
    # Check if from_timestamp in query_string.
    if 'from_timestamp' in query_string_dict:
        # Use the days ago in the from_timestamp.
        start_date_epoch = int(query_string_dict['from_timestamp'])
    else:
        # Default to 7 days ago.
        start_date_epoch = datetime.timestamp(datetime.utcnow() - timedelta(7))
    # Log for debugging.
    logger.debug(f'start_date_epoch: {start_date_epoch}')
    # Set our start_date from epoch.
    start_date = datetime.fromtimestamp(start_date_epoch)
    # Check if to_timestamp in query_string.
    if 'to_timestamp' in query_string_dict:
        # Use the days ago in the to_timestamp.
        end_date_epoch = int(query_string_dict['to_timestamp'])
    else:
        # Default to today.
        end_date_epoch = datetime.timestamp(datetime.utcnow())
    # Log for debugging.
    logger.debug(f'end_date_epoch: {end_date_epoch}')
    # Set our end_date from epoch.
    end_date = datetime.fromtimestamp(end_date_epoch)
    # Generate our date delta.
    date_delta = end_date - start_date
    # Loop through the count of days in our date_delta, we +1 to include the start date.
    for i in range(date_delta.days + 1):
        # Create our day.
        day = start_date + timedelta(days=i)
        # Log for debugging
        logger.debug(f'day: {day}')
        # Format the day.
        formatted_start_date = day.strftime('%m/%d')
        # Log for debugging.
        logger.debug(f'formatted_start_date: {formatted_start_date}')
        # Initialize our counters that we will increment.
        success_count = 0
        failed_count = 0
        # Loop through our log data to see if it is in the same day as our current item.
        for log in logs_data:
            # Get the date from the log.
            log_date = datetime.fromtimestamp(log['timestamp'])
            # Format the log the same as our dates.
            formatted_log_date = log_date.strftime('%m/%d')
            if formatted_log_date == formatted_start_date:
                if log['status'] == 'Deployed':
                    success_count = success_count + 1
                elif log['status'] == 'Failed':
                    failed_count = failed_count + 1
        # Append our formatted_start_date to our days list.
        daily_deploy_data.append({ 'date': formatted_start_date, 'success_count': success_count, 'failed_count': failed_count})
    logger.debug(f'daily_deploy_data: {daily_deploy_data}')


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
    return render_template(
        "analytics.html",
        daily_deploy_data=daily_deploy_data,
        applications=set(applications),
        services=set(services),
        environments=set(environments),
        query_string=query_string_dict,
        totalDailyDeploymentData=daily_deploy_data
    )


@analytics_page.route('/', methods=['POST'])
def analytics_search():
    """
    Redirects back to the analytics page, but appending the query string parameters from the form
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
    if 'daysago' in request.form:
        query_params['daysago'] = request.form['daysago']
    # Return the logs page with our query string parameters from request form.
    return redirect(url_for('analytics_page.analytics', **query_params))


def get_logs(query_string, token):
    try:
        response = requests.get(
            f'http://api:8081/logs?{query_string}',
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
            f'http://api:8081/services',
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
