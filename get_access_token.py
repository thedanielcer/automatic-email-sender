import os
import msal
from dotenv import set_key
from urllib.parse import urlparse, parse_qs

REDIRECT_URI = "http://localhost:8000"
ENV_PATH = ".env"

def get_access_token(client_id, client_secret, scopes):
    client = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority="https://login.microsoftonline.com/consumers"
    )

    refresh_token = os.getenv("refresh_token")

    if refresh_token:
        token_response = client.acquire_token_by_refresh_token(refresh_token, scopes=scopes)
    else:
        auth_request_url = client.get_authorization_request_url(
            scopes,
            redirect_uri=REDIRECT_URI
            )
        print(auth_request_url)
        redirected_url = input('Full URL: ')

        authorization_code = parse_qs(urlparse(redirected_url).query)["code"][0]

        if not authorization_code:
            raise ValueError("Authorization code is empty")
        
        token_response = client.acquire_token_by_authorization_code(
            code=authorization_code,
            scopes=scopes,
            redirect_uri=REDIRECT_URI
        )

    if 'access_token' in token_response:
        if 'refresh_token' in token_response:
            set_key(ENV_PATH, "refresh_token", token_response["refresh_token"])
        else:
            raise KeyError("Refresh token not found in token_response")
    else:
        raise KeyError("Access token not found in token_response: " + str(token_response))

    return token_response["access_token"]

