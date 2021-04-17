import json
import logging
from hashlib import sha256

logger = logging.getLogger(__name__)


def hash_dict(subject: dict):
    """
    sha256 hash a dict.
    """

    # json.dumps our dict with sort_keys so its always in the same order.
    json_string = json.dumps(subject, sort_keys=True)
    # log for debugging.
    logger.debug(f"json_string: {json_string}")

    # encode the json string to utf-8.
    encoded_json = json_string.encode("utf-8")
    # log for debugging.
    logger.debug(f"encoded_json: {encoded_json}")

    # sha256().hexdigest to get the hexidecimal string.
    final_hash = sha256(encoded_json).hexdigest()
    # log for debugging.
    logger.debug(f"final_hash: {final_hash}")

    return final_hash


def hash_string(subject: str):
    """
    sha256 hash a string.
    """

    # encode the json string to utf-8.
    encoded_subject = subject.encode("utf-8")
    # log for debugging.
    logger.debug(f"encoded_subject: {encoded_subject}")

    # sha256().hexdigest to get the hexidecimal string.
    final_hash = sha256(encoded_subject).hexdigest()
    # log for debugging.
    logger.debug(f"final_hash: {final_hash}")

    return final_hash
