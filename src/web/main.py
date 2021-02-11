import os
import logging
from flask import Flask, session, redirect, url_for, request
from flask_wtf.csrf import CSRFProtect
from routes.login import login_page
from routes.logout import logout_page
from routes.dashboard import dashboard_page
from routes.ci import ci_page
from routes.applications import applications_page
from routes.logs import logs_page
from routes.analytics import analytics_page
from routes.users import users_page
from routes.apikeys import apikeys_page
from routes.integrations import integrations_page
from routes.billing import billing_page
from routes.environments import environments_page
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET']
csrf = CSRFProtect(app)

app.register_blueprint(login_page, url_prefix='/login')
app.register_blueprint(logout_page, url_prefix='/logout')
app.register_blueprint(dashboard_page, url_prefix='/dashboard')
app.register_blueprint(ci_page, url_prefix='/ci')
app.register_blueprint(applications_page, url_prefix='/applications')
app.register_blueprint(logs_page, url_prefix='/logs')
app.register_blueprint(analytics_page, url_prefix='/analytics')
app.register_blueprint(users_page, url_prefix='/settings/users')
app.register_blueprint(apikeys_page, url_prefix='/settings/apikeys')
app.register_blueprint(integrations_page, url_prefix='/settings/integrations')
app.register_blueprint(billing_page, url_prefix='/settings/billing')
app.register_blueprint(environments_page, url_prefix='/settings/environments')


@app.route('/')
def index():
    # If user is logged in.
    if 'logged_in' in session:
        # We're logged in so go to dashboard.
        return redirect(url_for('dashboard_page.dashboard'))
    # We're not logged in so go to login page.
    return redirect(url_for('login_page.login'))


@app.before_request
def check_session_expired():
    """ Checks if session is expired """
    # If user is logged in.
    if 'logged_in' in session:
        # If session is not expired.
        # TODO: Remove this when refresh token is in place, we also need to apply this to all routes, not just index
        if session['exp'] < datetime.now().timestamp():
            # Clear the user's session.
            session.clear()
            # redirect to login page to clear session, which will redirect to login page.
            return redirect(url_for('logout_page.logout'))
    elif 'login' in request.base_url:
        # Ignore if /login
        pass
    elif 'static' in request.base_url:
        # Ignore if /static/*
        pass
    elif 'favicon' in request.base_url:
        # Ignore if /favicon.ico
        pass
    else:
        # Redirect all unauthenticated requests to the login page.
        return redirect(url_for('login_page.login'))


@app.template_filter()
def epoch_to_date(epoch):
    """ Converts epoch to timezone in user's profile """
    # TODO: Get timezone from the user's session, and convert to that.
    #  Need to first set it in user's session after login.
    # Log for debugging.
    logger.debug(f"epoch: {epoch}")
    # Set date from epoch.
    new_date = datetime.fromtimestamp(epoch)
    # Format the date.
    formatted_date = new_date.strftime('%m/%d/%Y %H:%M:%S')
    # Return the formatted date.
    return formatted_date


@app.context_processor
def inject_theme():
    """ Injects globals into Jinja templates """
    # Check if theme is in session.
    if 'theme' in session:
        # If theme in session, use the theme.
        theme = session['theme']
    else:
        theme = 'light'
    # Check that theme is either light or dark, in case someone manually changed session.
    if theme not in ['light', 'dark']:
        # Default to light.
        theme = 'light'
    return dict(theme=theme)


@app.route('/settings', methods=['GET'])
def settings():
    return redirect(url_for('users_page.users'))


if __name__ == "__main__":
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=os.getenv('FLASK_PORT', '8080'),
        debug=os.getenv('FLASK_DEBUG', False)
    )
