import os
import logging
import requests
from jose import jwt
from flask import Blueprint, render_template, request, session, redirect, url_for

login_page = Blueprint('login_page', __name__)

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ['APP_SECRET']
ALGORITHM = "HS256"


@login_page.route('/', methods=['GET'])
def login():
    return render_template("login.html", header=False)


@login_page.route('/', methods=['POST'])
def login_post():
    logger.debug(request.form)
    attempted_username = request.form['email']
    attempted_password = request.form['password']

    try:
        response = requests.post(
            'http://api:8081/token',
            data={
                'username': attempted_username,
                'password': attempted_password
            }
        )
        logger.debug(f'response: {response.status_code}')
        if response.status_code == 401:
            return render_template("login.html", header=False, error='Invalid Username or Password')

        token = response.json()['access_token']
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
    except Exception as error:
        logger.info(f'Type {type(error)}')
        logger.error(f'Exception: {error}')
        return render_template("login.html", header=False, error=error)
