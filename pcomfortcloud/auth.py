import hashlib
import json
import random
import string
import base64
import requests
import urllib
from datetime import datetime
from bs4 import BeautifulSoup
from . import session

auth_0_client = "eyJuYW1lIjoiQXV0aDAuQW5kcm9pZCIsImVudiI6eyJhbmRyb2lkIjoiMzAifSwidmVyc2lvbiI6IjIuOS4zIn0="
app_client_id = "Xmy6xIYIitMxngjB2rHvlm6HSDNnaMJx"
redirect = "panasonic-iot-cfc://authglb.digital.panasonic.com/android/com.panasonic.ACCsmart/callback"


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_random_string_hex(length):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


def get_new_token(username, password):
    requests_session = requests.Session()

    # generate state and code_challenge
    state = generate_random_string(20)

    code_verifier = generate_random_string(43)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(
            code_verifier.encode('utf-8')
        ).digest()).split('='.encode('utf-8'))[0].decode('utf-8')

    print("AUTHORIZE")
    # ------------------------------------------------------------------------------------------------------------------
    headers = {
        "user-agent": "okhttp/4.10.0",
    }

    params = {
        "scope": "openid offline_access comfortcloud.control a2w.control",
        "audience": f"https://digital.panasonic.com/{app_client_id}/api/v1/",
        "protocol": "oauth2",
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "auth0Client": auth_0_client,
        "client_id": app_client_id,
        "redirect_uri": redirect,
        "state": state,
    }

    response = requests_session.get(
        'https://authglb.digital.panasonic.com/authorize',
        headers=headers,
        params=params,
        allow_redirects=False)

    # get the "state" querystring parameter from the redirect url
    location = response.headers['Location']
    parsed_url = urllib.parse.urlparse(location)
    params = urllib.parse.parse_qs(parsed_url.query)
    state_value = params.get('state', [None])[0]
    print('state: ' + state_value)

    print("FOLLOW REDIRECT")
    # ------------------------------------------------------------------------------------------------------------------
    headers = {
        "user-agent": "okhttp/4.10.0",
    }

    response = requests_session.get(
        f"https://authglb.digital.panasonic.com{location}",
        allow_redirects=False)

    # get the "_csrf" cookie
    csrf = response.cookies['_csrf']
    print('_csrf: ' + csrf)

    print("LOGIN")
    # ------------------------------------------------------------------------------------------------------------------
    headers = {
        "Auth0-Client": auth_0_client,
        "user-agent": "okhttp/4.10.0",
    }

    data = {
        "client_id": app_client_id,
        "redirect_uri": redirect,
        "tenant": "pdpauthglb-a1",
        "response_type": "code",
        "scope": "openid offline_access comfortcloud.control a2w.control",
        "audience": f"https://digital.panasonic.com/{app_client_id}/api/v1/",
        "_csrf": csrf,
        "state": state_value,
        "_intstate": "deprecated",
        "username": username,
        "password": password,
        "lang": "en",
        "connection": "PanasonicID-Authentication"
    }

    response = requests_session.post(
        'https://authglb.digital.panasonic.com/usernamepassword/login',
        headers=headers,
        json=data,
        allow_redirects=False)

    # get wa, wresult, wctx from body
    soup = BeautifulSoup(response.content, "html.parser")
    input_lines = soup.find_all("input", {"type": "hidden"})
    parameters = dict()
    for input_line in input_lines:
        parameters[input_line.get("name")] = input_line.get("value")

    auth_0_request_id = response.headers['X-Auth0-RequestId']
    print("Auth0-RequestId: " + auth_0_request_id)

    print("CALLBACK")
    # ------------------------------------------------------------------------------------------------------------------
    user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
    user_agent += "(KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36"

    response = requests_session.post(
        url="https://authglb.digital.panasonic.com/login/callback",
        data=parameters,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": user_agent,
        },
        allow_redirects=False)

    print("FOLLOW REDIRECT")
    # ------------------------------------------------------------------------------------------------------------------
    headers = {
        "user-agent": "okhttp/4.10.0",
    }

    location = response.headers['Location']
    response = requests_session.get(
        f"https://authglb.digital.panasonic.com{location}",
        allow_redirects=False)

    location = response.headers['Location']
    parsed_url = urllib.parse.urlparse(location)
    params = urllib.parse.parse_qs(parsed_url.query)
    code = params.get('code', [None])[0]
    print('code: ' + code)

    print("GET TOKEN")
    # ------------------------------------------------------------------------------------------------------------------
    headers = {
        "Auth0-Client": auth_0_client,
        "user-agent": "okhttp/4.10.0",
    }

    data = {
        "scope": "openid",
        "client_id": app_client_id,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect,
        "code_verifier": code_verifier
    }

    response = requests_session.post(
        'https://authglb.digital.panasonic.com/oauth/token',
        headers=headers,
        json=data,
        allow_redirects=False)
    token = json.loads(response.text)
    return token


def get_user_info(self):
    if self._raw:
        print("--- Getting User Info")

    response = None

    try:
        response = requests.get(
            'https://authglb.digital.panasonic.com/userinfo',
            headers={
                "Auth0-Client": auth_0_client,
                "Authorization": "Bearer " + self._token["access_token"]
            })

        if 2 != response.status_code // 100:
            raise session.ResponseError(response.status_code, response.text)

    except requests.exceptions.RequestException as ex:
        raise session.RequestError(ex)


def get_header_for_api_calls(self):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    return {
        "Content-Type": "application/json;charset=utf-8",
        "X-APP-NAME": "Comfort Cloud",
        "User-Agent": "G-RAC",
        "X-APP-TIMESTAMP": timestamp,
        "X-APP-TYPE": "1",
        "X-APP-VERSION": "1.20.0",
        # "X-CFC-API-KEY": "0",
        "X-CFC-API-KEY": generate_random_string_hex(128),
        "X-Client-Id": self._acc_client_id,
        "X-User-Authorization-V2": "Bearer " + self._token["access_token"]
    }


def refresh_token(self):
    if self._raw:
        print("--- Refreshing Token")

    headers = {
        "Auth0-Client": auth_0_client,
        "user-agent": "okhttp/4.10.0",
    }

    data = {
        "grant_type": "refresh_token",
        "client_id": app_client_id,
        "refresh_token": self._token["refresh_token"],
    }

    try:
        response = requests.post(
            'https://authglb.digital.panasonic.com/oauth/token',
            headers=headers,
            json=data,
            allow_redirects=False
        )

        if 2 != response.status_code // 100:
            raise session.ResponseError(response.status_code, response.text)

    except requests.exceptions.RequestException as ex:
        raise session.RequestError(ex)

    token = json.loads(response.text)
    return token


def login(self):
    response = requests.post(
        'https://accsmart.panasonic.com/auth/v2/login',
        headers=get_header_for_api_calls(self),
        json={
            "language": 0
        })

    json_response = json.loads(response.content)
    self._acc_client_id = json_response["clientId"]
