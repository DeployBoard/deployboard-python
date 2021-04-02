import logging
from jose import jwt
from flask import Blueprint, render_template, request, session, redirect, url_for
from webutil.webapi import webapi
from webutil.config import config

login_page = Blueprint('login_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = config('APP_SECRET')
ALGORITHM = "HS256"


@login_page.route('/', methods=['GET'])
def login():
    if 'logged_in' in session:
        logger.debug("User logged_in so go to dashboard.")
        return redirect(url_for('dashboard_page.dashboard'))
    return render_template("login.html", header=False)


@login_page.route('/', methods=['POST'])
def login_post():
    logger.debug(f'request form: {request.form}')
    attempted_username = request.form['email']
    data = {
        'username': attempted_username,
        'password': request.form['password']
    }
    try:
        # Call our api endpoint.
        response = webapi('post', 'token/', data=data)
        # Log response for debugging.
        logger.debug(f'response: {response}')
    except Exception as e:
        # Log exception.
        logger.error(f'Exception: {e}')
        # Return our page with error.
        return render_template("login.html", header=False, error=e)

    token = response['access_token']
    logger.debug(f'token: {token}')

    # Decode our jwt from response - this holds our user's information
    token_decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    logger.info(f'token_decoded: {token_decoded}')  # TODO: The id is in the sub, should it be email?

    # TODO: we should make a second api call here to get the user's info and store it in the session
    session['token'] = token  # TODO: we need to store the token in httponly cookie, not in session.
    session['logged_in'] = True
    session['user_id'] = token_decoded['sub']
    session['exp'] = token_decoded['exp']  # TODO: Possibly remove this when refresh token is in place
    session['username'] = attempted_username

    logger.info(f'session: {session}')

    return redirect(url_for('dashboard_page.dashboard'))
