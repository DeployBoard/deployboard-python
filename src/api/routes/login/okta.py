import logging

import requests
from fastapi import HTTPException

logger = logging.getLogger(__name__)


# Call the Okta API to get an access token
def retrieve_okta_token(authorization, issuer, scope="email"):
    headers = {
        "accept": "application/json",
        "authorization": authorization,
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials", "scope": scope}
    url = issuer + "/v1/token"

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail=response.text)
