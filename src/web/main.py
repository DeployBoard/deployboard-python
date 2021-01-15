import os
import logging
from flask import Flask, session, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from routes.login import login_page
from routes.logout import logout_page
from routes.dashboard import dashboard_page
from routes.ci import ci_page
from routes.applications import applications_page
from routes.logs import logs_page
from routes.users import users_page
from routes.apikeys import apikeys_page
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
app.register_blueprint(users_page, url_prefix='/settings/users')
app.register_blueprint(apikeys_page, url_prefix='/settings/apikeys')


@app.route('/')
def index():
    # If user is logged in.
    if 'logged_in' in session:
        # If session is not expired.
        # TODO: Remove this when refresh token is in place, we also need to apply this to all routes, not just index
        if session['exp'] < datetime.now().timestamp():
            # redirect to login page to clear session, which will redirect to login page.
            return redirect(url_for('logout_page.logout'))
        # We're logged in so go to dashboard.
        return redirect(url_for('dashboard_page.dashboard'))
    # We're not logged in so go to login page.
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


@app.route('/settings', methods=['GET'])
def settings():
    return redirect(url_for('users_page.users'))


if __name__ == "__main__":
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=os.getenv('FLASK_PORT', '8080'),
        debug=os.getenv('FLASK_DEBUG', False)
    )