import logging
from fastapi import HTTPException
from util.account import get_account

logger = logging.getLogger(__name__)


def check_password_policy(account: str, password: str):
    """
    Verifies a password satisfies the specified policy.
    """
    logger.debug(f"account: {account}")
    logger.debug(f"password: {password}")

    # Get our account info.
    account_response = get_account(account)
    # Log account_response for debugging.
    logger.debug(f"account_response: {account_response}")
    # Get the password_policy from our account response.
    policy = account_response['password_policy']

    # Perform our checks of the supplied password against the policy.
    # Create this status object so we can return the status of all tests to the caller.
    status = {
        'length': check_length(password, policy['length']),
        'lowercase': check_lowercase(password, policy['lowercase']),
        'uppercase': check_uppercase(password, policy['uppercase']),
        'number': check_number(password, policy['number']),
        'special': check_special(password, policy['special'])
    }
    # Log status for debugging.
    logger.debug(f"status: {status}")
    # TODO: Implement way to check if new password is same as old password.
    # We probably have to hash the current password with the previous salt + pepper then compare the hashes.
    # check_previous(password, previous_password_hash)

    # Default our summary to True. We'll update later if we find issues.
    summary = True
    # Loop through our status key value pairs and see if we had any failures.
    for key in status:
        if status[key] is False:
            summary = False
    # Check if our updated summary is now False.
    if summary is False:
        # Log that password did not meet policy.
        logger.info("Password does not meet the policy.")
        # Raise an exception because the password provided did not meet the account's policy.
        raise HTTPException(status_code=400, detail=f"Password does not meet the policy: {policy}")

    return {'summary': summary, 'status': status}


def check_length(password, requirement):
    """
    Checks if the password has required length.
    """
    # If the length of the password is less than the requirement, fail.
    if len(password) < requirement:
        return False
    return True


def check_lowercase(password, requirement):
    """
    Checks if the password has required count of lowercase characters.
    """
    # Initialize our counter.
    count = 0
    # Loop over each character in the string.
    for character in password:
        # If that character is lowercase, increment the counter.
        if character.islower():
            count += 1
    # If the count of lowercase letters is less than the requirement, fail.
    if count < requirement:
        return False

    return True


def check_uppercase(password, requirement):
    """
    Checks if the password has required count of uppercase characters.
    """
    # Initialize our counter.
    count = 0
    # Loop over each character in the string.
    for character in password:
        # If that character is uppercase, increment the counter.
        if character.isupper():
            count += 1
    # If the count of uppercase letters is less than the requirement, fail.
    if count < requirement:
        return False

    return True


def check_number(password, requirement):
    """
    Checks if the password has required count of numeric characters.
    """
    # Initialize our counter.
    count = 0
    # Loop over each character in the string.
    for character in password:
        # If that character is numeric, increment the counter.
        if character.isnumeric():
            count += 1
    # If the count of numeric characters is less than the requirement, fail.
    if count < requirement:
        return False

    return True


def check_special(password, requirement):
    """
    Checks if the password has required count of special characters.
    """
    # Define the special characters we want to support.
    special_characters = [
        " ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+",
        ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[",
        "\\", "]", "^", "_", "`", "{", "|", "}", "~"
    ]
    # Initialize our counter.
    count = 0
    # Loop over each character in the string.
    for character in password:
        # If that character is special, increment the counter.
        if character in special_characters:
            count += 1
    # If the count of numeric characters is less than the requirement, fail.
    if count < requirement:
        return False

    return True
