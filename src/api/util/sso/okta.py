import asyncio
import json
import logging
from datetime import datetime

import requests
from db.mongo import db
from fastapi import HTTPException
from okta_jwt.jwt import validate_token
from util.config import config

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


def verify_okta_code(code):
    # Construct our request to validate our code and get our token.
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    query_params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config("OKTA_REDIRECT_URL"),
    }
    query_params = requests.compat.urlencode(query_params)

    # Make the request with our code to get an Okta token.
    try:
        exchange = requests.post(
            config("OKTA_TOKEN_URL"),
            headers=headers,
            data=query_params,
            auth=(config("OKTA_CLIENT_ID"), config("OKTA_CLIENT_SECRET")),
        ).json()
        # Log exchange for debugging.
        logger.debug(f"exchange: {exchange}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return a nice error.
        return "An error occurred during the Okta code exchange.", 403

    # Get tokens and validate.
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403

    # Validate access token.
    access_token = exchange["access_token"]
    decoded_access_token = validate_token(
        access_token, config("OKTA_ISSUER"), "api://default", config("OKTA_CLIENT_ID")
    )
    # Log our decoded access token for debugging.
    logger.debug(f"decoded_access_token: {decoded_access_token}")

    if not decoded_access_token:
        return "Access token is invalid.", 403

    # TODO: Also validate the ID token, but until then we are getting information
    #  about the user from the /userinfo url, so we don't need to

    # Authorization flow successful, get userinfo and login user
    try:
        userinfo_response = requests.get(
            config("OKTA_USERINFO_URL"),
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()
        # Log our userinfo_response for debugging.
        logger.debug(f"userinfo_response: {userinfo_response}")
    except Exception as e:
        # Log exception.
        logger.error(f"Exception: {e}")
        # Return a nice error.
        return "An error occurred while getting userinfo from Okta.", 403

    # Check our role mapping from the config and set our user's role.
    assign_user_role = check_okta_role_mapping(userinfo_response["groups"])
    logger.debug(f"assign_user_role: {assign_user_role}")

    verified_user = put_okta_user_in_db(userinfo_response, assign_user_role)

    create_account_if_first_user(userinfo_response["email"].split("@")[1])

    # Return a dictionary of our user, right now only _id and email is needed.
    return {"_id": verified_user["_id"], "email": verified_user["email"]}


def check_okta_role_mapping(user_roles):
    """
    Gets role mapping from config and checks okta user's groups. Returns a role.
    """

    # Init our empty matched roles list.
    matched_roles = []
    # Get the Okta role mapping from config.
    role_map = json.loads(config("OKTA_ROLE_MAPPING"))
    for user_role in user_roles:
        logger.debug(f"checking role mapping for {user_role}")
        logger.debug(f"checking if {user_role} in {role_map.keys()}")
        if user_role in role_map.keys():
            matched_roles.append(user_role)

    logger.debug(f"matched_roles: {matched_roles}")

    # Init our final user_role at the lowest and default level of Viewer.
    user_final_role = "Viewer"
    # Check the role mapping.
    for role in matched_roles:
        logger.debug(f"role_map[role]: {role_map[role]}")
        match role_map[role]:
            case "Admin":
                user_final_role = "Admin"
                # If we match for Admin we can just stop looking.
                break
            case "Editor":
                user_final_role = "Editor"
            # If we don't match anything we'll end up using the default role of Viewer.

    return user_final_role


def put_okta_user_in_db(userinfo, role):
    """
    Creates or updates user in the db.
    """
    # Generate an epoch to use for created and modified timestamp.
    ts = datetime.utcnow().timestamp()
    try:
        # Update or Upsert our user in the db.
        # TODO: Use an sso user schema for this insert.
        resp = db.users.update_one(
            {"email": userinfo["email"]},
            {
                "$set": {
                    "schema_version": 1,
                    "account": userinfo["email"].split("@")[1],
                    "email": userinfo["email"],
                    "role": role,
                    "first_name": userinfo["given_name"],
                    "last_name": userinfo["family_name"],
                    "locale": userinfo["locale"],
                    "zoneinfo": userinfo["zoneinfo"],
                    "enabled": True,
                    "last_logged_in": ts,
                    "sso": "okta",
                    "sso_sub": userinfo["sub"],
                }
            },
            upsert=True,
        )
        # Log for debugging.
        logger.debug(f"users.update_one matched_count: {resp.matched_count}")
        logger.debug(f"users.update_one modified_count: {resp.modified_count}")
        logger.debug(f"users.update_one upserted_id: {resp.upserted_id}")
        logger.debug(f"users.update_one raw_result: {resp.raw_result}")
    except Exception as e:
        # Log error
        logger.error(f"Exception: {e}")
        # Raise exception if user not found.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    if resp.upserted_id is not None:
        return {"_id": resp.upserted_id, "email": userinfo["email"]}
    else:
        return {
            "_id": get_okta_user_id(userinfo["email"], userinfo["sub"], "okta"),
            "email": userinfo["email"],
        }


def get_okta_user_id(email, sso_sub, sso):
    """
    Since and update_one doesn't return the updated _id, we need to fetch it ourselves.
    """

    try:
        # Attempt to find our user in the database by email.
        # TODO: Use an sso user schema for this insert.
        resp = db.users.find_one({"email": email, "sso_sub": sso_sub, "sso": sso})
        # Log for debugging.
        logger.debug(f"users.find_one resp: {resp}")
        logger.debug(f"users.find_one _id: {resp['_id']}")
    except Exception as e:
        # Log error
        logger.error(f"Exception: {e}")
        # Raise exception if user not found.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    # Have to return the ObjectId as a string.
    return str(resp["_id"])


def create_account_if_first_user(account):
    """
    Creates the account in the db if this is the first user logging in.
    """
    # Set our query for the update.
    query = {"account": account}

    try:
        # Attempt to find our account in the database.
        resp = db.accounts.find_one(query)
        # Log for debugging.
        logger.debug(f"accounts.find_one resp: {resp}")
    except Exception as e:
        # Log error
        logger.error(f"Exception: {e}")
        # Raise exception if user not found.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    # If we have an empty response, we'll want to create the account.
    if resp is None:
        create_account(account)


def create_account(account):
    """
    Creates the account in the db.
    Returns True if we created a new account.
    Returns False if we did not create a new account.
    """
    # Generate an epoch to use for created and modified timestamp.
    ts = datetime.utcnow().timestamp()

    try:
        # Attempt to find our account in the database.
        resp = db.accounts.insert_one(
            {
                "schema_version": 1,
                "account": account,
                "auth": "Okta",
                "created_timestamp": ts,
                "environments": [],
            }
        )
        # Log for debugging.
        logger.debug(f"accounts.find_one inserted_id: {resp.inserted_id}")
    except Exception as e:
        # Log error
        logger.error(f"Exception: {e}")
        # Raise exception if user not found.
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    # If we don't have an empty response we'll return True.
    if resp is not None:
        return True
    else:
        return False
