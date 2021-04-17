import os


def config(param):
    """
    Returns our config object after reading environment for overrides.
    """
    # Initialize our config.
    config_dic = {
        "LOG_LEVEL": "warn",
        "DPB_WEB_HOST": "0.0.0.0",
        "DPB_WEB_PORT": "8080",
        "DPB_WEB_DEBUG": False,
        "DPB_API_URI": "http://api:8081",
        "APP_SECRET": "changeme",
    }

    # Loop through our defaults.
    for item in config_dic:
        # Check if the item is in the environment.
        if item in os.environ:
            # Override the default with what is in the environment.
            config_dic[item] = os.environ[item]

    return config_dic[param]
