import os


def config(param):
    """
    Returns our config object after reading environment for overrides.
    """
    # Initialize our config.
    config_dic = {
        "MONGO_URI": None,
        "MONGO_DATABASE": "deployboard"
    }

    # Loop through our defaults.
    for item in config_dic:
        # Check if the item is in the environment.
        if item in os.environ:
            # Override the default with what is in the environment.
            config_dic[item] = os.environ[item]

    return config_dic[param]
