import logging
import os
import secrets
from datetime import datetime, timedelta
from random import randint, random

from passlib.context import CryptContext
from pymongo import MongoClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get our mongo settings from environment
mongo_uri = os.environ["MONGO_URI"] if "MONGO_URI" in os.environ else "localhost:27017"
database = (
    os.environ["MONGO_DATABASE"] if "MONGO_DATABASE" in os.environ else "deployboard"
)
mongo_client = MongoClient(mongo_uri)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Check if our db exists.
if database in mongo_client.list_database_names():
    # The db exists, so we will drop it.
    mongo_client.drop_database(database)
# Creating a connection to a non-existent database will create it.
db = mongo_client[database]


def create_account():
    """
    Creates account.
    """
    # Log for debugging.
    logger.debug("creating account")
    # Define our account.
    account_dict = {
        "schema_version": 1.0,
        "account": "Example",
        "environments": ["Prod", "Stage", "Dev"],
        "created_timestamp": 1610053395,
        "password_policy": {
            "length": 6,
            "lowercase": 0,
            "uppercase": 0,
            "number": 0,
            "special": 0,
        },
    }
    # Insert the user into the db.
    insert_resp = db.accounts.insert_one(account_dict)
    # Log for debugging.
    logger.debug(f"insert_resp: {insert_resp.inserted_id}")
    return insert_resp.inserted_id


def create_user(user_role, enabled):
    """
    Creates our first user.
    """
    # Log for debugging.
    logger.debug(f"creating user for: {user_role}")
    # Set our email.
    if enabled:
        email = f"{user_role.lower()}@example.com"
    else:
        email = f"disabled{user_role.lower()}@example.com"

    # Generate salt and hashed_password.
    password = "secret"
    salt = secrets.token_hex(16)
    pepper = os.environ["PEPPER"] if "PEPPER" in os.environ else "changeme"
    password_hash = pwd_context.hash(password + salt + pepper)

    # Define our user.
    user_dict = {
        "schema_version": 1.0,
        "account": "Example",
        "salt": salt,
        "hashed_password": password_hash,
        "password_expires": 1610053395,
        "email": email,
        "role": user_role,
        "first_name": "John",
        "last_name": "Doe",
        "enabled": enabled,
        "created_timestamp": 1610053395,
        "modified_timestamp": 1610053395,
        "modified_by": "admin@example.com",
    }
    # Insert the user into the db.
    insert_resp = db.users.insert_one(user_dict)
    # Log for debugging.
    logger.debug(f"insert_resp: {insert_resp.inserted_id}")
    return insert_resp.inserted_id


def create_api_key(api_key_role):
    """
    Creates api key.
    """
    # Log for debugging.
    logger.debug(f"creating api key for: {api_key_role}")
    # Define our api key.
    api_key_dict = {
        "schema_version": 1.0,
        "account": "Example",
        "name": "test-api-key",
        "role": api_key_role,
        "enabled": True,
        "created_by": "jdoe@example.com",
        "created_timestamp": 1610053395,
        "modified_by": "admin@example.com",
        "modified_timestamp": 1610053395,
    }
    # Insert the user into the db.
    insert_resp = db.apikeys.insert_one(api_key_dict)
    # Log for debugging.
    logger.debug(f"insert_resp: {insert_resp.inserted_id}")
    return insert_resp.inserted_id


def create_service(application, service):
    """
    Creates service.
    """
    # Log for debugging.
    logger.debug("creating service")
    # Define our service.
    service_dict = {
        "schema_version": 1.0,
        "service": service,
        "application": application,
        "account": "Example",
        "tags": ["python"],
        "environments": {
            "Dev": {
                "status": "Deployed",
                "version": "1.3.0",
                "timestamp": 1608433640,
                "custom": {"module": "foo", "color": "green"},
            },
            "Stage": {
                "status": "Deployed",
                "version": "1.2.1",
                "timestamp": 1608523640,
                "custom": {"module": "foo", "color": "green"},
            },
            "Prod": {
                "status": "Deployed",
                "version": "1.2.0",
                "timestamp": 1608623640,
                "custom": {"module": "foo", "color": "green"},
            },
        },
    }
    # Insert the user into the db.
    insert_resp = db.services.insert_one(service_dict)
    # Log for debugging.
    logger.debug(f"insert_resp: {insert_resp.inserted_id}")
    return insert_resp.inserted_id


def create_logs(application, service, days_ago):
    """
    Creates logs.
    """
    # TODO: Increase the version with each deployment instead of generating random int.
    # Log for debugging.
    logger.debug("creating logs")
    # Instantiate our logs list.
    logs_list = []
    # for days_ago generate datetime object
    # Generate a list of log dicts each time incrementing the version,
    # and the timestamp.
    for day in range(days_ago):
        for env in ["Dev", "Stage", "Prod"]:
            # Generate a random version number for this deployment.
            version = f"{randint(0, 9)}.{randint(0, 50)}.{randint(0, 9)}"
            # Generate our date object.
            start_date = datetime.utcnow() - timedelta(days=day)
            # Convert it to epoch for our start timestamp.
            start_timestamp = start_date.timestamp()
            # Append our start time (Deploying).
            # TODO: properly generate the hashes.
            logs_list.append(
                {
                    "schema_version": 1.0,
                    "service": service,
                    "application": application,
                    "account": "Example",
                    "environment": env,
                    "status": "Deploying",
                    "version": version,
                    "timestamp": start_timestamp,
                    "hash": (
                        "a7cd6c222ea5fc1463c0ca3f70b93035"
                        "196c8c4f34d89181ff5086bd7b58bfff"
                    ),
                    "hash_chain": (
                        "6a9ec5bf3b15354e1cb8599e2262a9ff"
                        "8d808d793987399bb9bd41c949cd661a"
                    ),
                    "custom": {"module": "foo", "color": "green"},
                }
            )
            # Add a random time to our start date to give us a stop date.
            stop_date = start_date + timedelta(minutes=randint(1, 10))
            # Convert our stop date to epoch for our stop timestamp.
            stop_timestamp = stop_date.timestamp()
            # Set finished status as Failed 20% of the time.
            if random() < 0.2:
                finished_status = "Failed"
            else:
                finished_status = "Deployed"
            # Append our stop time (Deployed).
            # TODO: properly generate the hashes.
            logs_list.append(
                {
                    "schema_version": 1.0,
                    "service": service,
                    "application": application,
                    "account": "Example",
                    "environment": env,
                    "status": finished_status,
                    "version": version,
                    "timestamp": stop_timestamp,
                    "hash": (
                        "a7cd6c222ea5fc1463c0ca3f70b93035"
                        "196c8c4f34d89181ff5086bd7b58bfff"
                    ),
                    "hash_chain": (
                        "6a9ec5bf3b15354e1cb8599e2262a9ff"
                        "8d808d793987399bb9bd41c949cd661a"
                    ),
                    "custom": {"module": "foo", "color": "green"},
                }
            )
    # Log for debugging.
    # logger.debug(f"logs_list: {logs_list}")
    # Insert the logs_list into the db.
    insert_resp = db.logs.insert_many(logs_list)
    # Log for debugging.
    logger.debug(f"insert_resp: {insert_resp}")
    # return inserted_ids
    return insert_resp.inserted_ids


def seed():
    # Instantiate our return dict with our account creation.
    response_dict = {"account": create_account()}

    # Instantiate our users dict.
    users_dict = {}
    # Instantiate our api_key dict.
    api_keys_dict = {}

    # Create a user and api key for each role.
    for role in ["Viewer", "Editor", "Admin"]:
        # Create the enabled users.
        users_dict[role] = create_user(role, True)
        # Create the disabled users.
        users_dict[f"disabled{role}"] = create_user(role, False)
        # Create the api key.
        api_keys_dict[role] = create_api_key(role)

    # Add users_dict to our return_dict.
    response_dict["users"] = users_dict
    # Add api_keys_dict to our return_dict.
    response_dict["api_keys"] = api_keys_dict

    # Create list of application/service combo dicts.
    application_services = [
        {"application": "Sample", "service": "Api"},
        {"application": "Sample", "service": "Web"},
        {"application": "Admin", "service": "Api"},
        {"application": "Admin", "service": "Web"},
    ]
    # Write a service object in the db for each item in the list.
    for item in application_services:
        # Write the service in the db.
        response_dict["service"] = create_service(item["application"], item["service"])
        # Write the logs to the db.
        response_dict["logs"] = create_logs(item["application"], item["service"], 120)

    logger.info(f"response_dict: {response_dict}")

    return response_dict


if __name__ == "__main__":
    seed()
