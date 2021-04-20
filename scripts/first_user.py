import os
import secrets
from datetime import datetime
from getpass import getpass

from passlib.context import CryptContext
from pymongo import MongoClient

# Get our mongo settings from environment
mongo_uri = os.environ["MONGO_URI"] if "MONGO_URI" in os.environ else "localhost:27017"
database = (
    os.environ["MONGO_DATABASE"] if "MONGO_DATABASE" in os.environ else "deployboard"
)

mongo_client = MongoClient(mongo_uri)
# Creating a connection to a non-existent database will create it.
db = mongo_client[database]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gather_input():
    print(
        """
        ################################################################################
        # Welcome to the first user seed script.                                       #
        # We will create your top level account and first administrator user.          #
        #                                                                              #
        # If you have not already, you should read through the configuration options   #
        # to set a pepper that we will use to encrypt user passwords.                  #
        # We will be using these settings within this script. To avoid having to       #
        # change settings later, we recommend setting these first.                     #
        #                                                                              #
        # WARNING: This script will update existing resources if they already exist.   #
        #                                                                              #
        # Read more at https://docs.deployboard.io/deployment/configuration/           #
        ################################################################################
        """
    )
    input("    If you are ready to continue, press <return>")

    print("")
    print(
        """
    Enter the name of the account, this is often the name of your organization.
    """
    )
    account = input("Account: ")

    print(
        """

    Enter the name of the first administrator user.
    For notification purposes, this should be an email address.
    For recovery purposes, it is recommended to use distribution list.
    """
    )
    username = input("Username: ")

    print(
        """

    Enter a password for the admin user.
    """
    )
    password = getpass()

    print(
        """

    The pepper needs to match what is running in the config,
    or you won't be able to log in.
    Enter a pepper used to hash the password.
    """
    )
    pepper = getpass(prompt="Pepper: ")

    return {
        "account": account,
        "username": username,
        "password": password,
        "pepper": pepper,
    }


def create_account(account, today):
    """
    Creates account.
    """
    # Log for debugging.
    print(f"Creating Account: {account}")
    # Define our account.
    account_dict = {
        "schema_version": 1.0,
        "account": account,
        "environments": ["Prod", "Dev"],
        "created_timestamp": int(today),
        "password_policy": {
            "length": 6,
            "lowercase": 0,
            "uppercase": 0,
            "number": 0,
            "special": 0,
        },
    }
    # Format our query.
    query = {"account": account}
    # Insert the account into the db.
    response = db.accounts.update_one(query, {"$set": account_dict}, upsert=True)
    # Check the response and print some nice output for the user.
    if response.upserted_id:
        print("Created successfully.")
    elif response.modified_count > 0:
        print("Account already existed. Updated existing account.")
    else:
        print(f"Something unexpected happened: {response.raw_result}")
    return response.raw_result


def create_user(account, username, password, pepper, today):
    """
    Creates our first user.
    """
    # Log for debugging.
    print(f"Creating User: {username} in Account: {account}")
    # Generate salt and hashed_password.
    salt = secrets.token_hex(16)
    password_hash = pwd_context.hash(password + salt + pepper)

    # Define our user.
    user_dict = {
        "schema_version": 1.0,
        "account": account,
        "salt": salt,
        "hashed_password": password_hash,
        "password_expires": 9999999999,
        "email": username,
        "role": "Admin",
        "first_name": "",
        "last_name": "",
        "enabled": True,
        "created_timestamp": today,
        "modified_timestamp": today,
        "modified_by": username,
    }
    # Format our query.
    query = {"account": account, "email": username}
    # Insert the user into the db.
    response = db.users.update_one(query, {"$set": user_dict}, upsert=True)
    # Check the response and print some nice output for the user.
    if response.upserted_id:
        print("Created successfully.")
    elif response.modified_count > 0:
        print("User already existed. Updated existing user.")
    else:
        print(f"Something unexpected happened: {response.raw_result}")
    return response.raw_result


def first_user():
    # Gather the input from the user.
    user_input = gather_input()
    print("")
    # Generate our timestamp for today.
    today = int(datetime.utcnow().timestamp())
    # Create the account in the db.
    create_account(user_input["account"], today)
    print("")
    # Create the admin user in the db.
    create_user(
        user_input["account"],
        user_input["username"],
        user_input["password"],
        user_input["pepper"],
        today,
    )


if __name__ == "__main__":
    first_user()
