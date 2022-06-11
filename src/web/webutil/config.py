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
        "OKTA_ENABLED": True,
        "OKTA_CLIENT_ID": "0oa3n29kw3acmhPLH5d7",
        "OKTA_CLIENT_SECRET": "M8Tbe3bO1GZbwjV4ShkoijDf-oIQXXcageirAxCb",
        "OKTA_AUTH_URL": "https://dev-67537191.okta.com/oauth2/default/v1/authorize",
        "OKTA_TOKEN_URL": "https://dev-67537191.okta.com/oauth2/default/v1/token",
        "OKTA_USERINFO_URL": "https://dev-67537191.okta.com/oauth2/default/v1/userinfo",
        "OKTA_ISSUER": "https://dev-67537191.okta.com/oauth2/default",
        "OKTA_REDIRECT_URL": "http://localhost:80/login/okta/callback",
        "OKTA_SCOPES": "openid profile email groups",
        "OKTA_ALLOWED_DOMAINS": "",
        "OKTA_ALLOWED_GROUPS": "",
        "OKTA_ROLE_ATTRIBUTE_PATH": "",
    }

    # Loop through our defaults.
    for item in config_dic:
        # Check if the item is in the environment.
        if item in os.environ:
            # Override the default with what is in the environment.
            config_dic[item] = os.environ[item]

    return config_dic[param]
