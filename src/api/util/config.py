import os


def config(param):
    """
    Returns our config object after reading environment for overrides.
    """
    # Initialize our config.
    config_dic = {
        "MONGO_URI": None,
        "MONGO_DATABASE": "deployboard",
        "LOG_LEVEL": "WARNING",
        "APP_SECRET": "changeme",
        "DPB_PEPPER": "changeme",
        "DPB_PASSWORD_EXPIRES": 90,
        "OKTA_ENABLED": True,
        "OKTA_CLIENT_ID": "0oa3n29kw3acmhPLH5d7",
        "OKTA_CLIENT_SECRET": "M8Tbe3bO1GZbwjV4ShkoijDf-oIQXXcageirAxCb",
        "OKTA_API_BASE_URL": "https://dev-67537191.okta.com/oauth2/default",
        "OKTA_AUTH_URL": "https://dev-67537191.okta.com/oauth2/default/v1/authorize",
        "OKTA_TOKEN_URL": "https://dev-67537191.okta.com/oauth2/default/v1/token",
        "OKTA_USERINFO_URL": "https://dev-67537191.okta.com/oauth2/default/v1/userinfo",
        "OKTA_ISSUER": "https://dev-67537191.okta.com/oauth2/default",
        "OKTA_REDIRECT_URL": "http://localhost:80/login/okta/callback",
        "OKTA_SCOPES": "openid profile email groups",
        "OKTA_ALLOWED_DOMAINS": "TODO",
        "OKTA_ALLOWED_GROUPS": "TODO",
        "OKTA_ROLE_MAPPING": '{"Engineering": "User", "DevOps": "Admin"}',
    }

    # Loop through our defaults.
    for item in config_dic:
        # Check if the item is in the environment.
        if item in os.environ:
            # Override the default with what is in the environment.
            config_dic[item] = os.environ[item]

    return config_dic[param]
