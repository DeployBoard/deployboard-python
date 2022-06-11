from webutil.config import config


def check_sso_provider():
    # Init sso as None.
    sso = None
    if config("OKTA_ENABLED"):
        sso = {"link": "/login/okta", "name": "Okta"}
    return sso
