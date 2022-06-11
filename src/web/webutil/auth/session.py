from flask import session


def set_session(token, logged_in, user_id, exp, username, auth_method):
    # Sets some required session attributes.
    # TODO: we should make a second api call here to get the user's info
    #  and store it in the session
    # TODO: we need to store the token in httponly cookie, not in session.
    session["token"] = token
    session["logged_in"] = logged_in
    session["user_id"] = user_id
    # TODO: Possibly remove this exp when refresh token is in place
    session["exp"] = exp
    session["username"] = username
    session["auth_method"] = auth_method
