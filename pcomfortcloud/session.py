import os
import json
from pathlib import Path  

from .authentication import Authentication
from .apiclient import ApiClient
from . import constants

class Session(Authentication):
    """ Verisure app session

    Args:
        username (str): Username used to login to verisure app
        password (str): Password used to login to verisure app

    """

    def __init__(self, username, password, tokenFileName='$HOME/.panasonic-oauth-token', raw=False):
        super().__init__(username, password, None, raw)

        home = str(Path.home())
        self._tokenFileName = os.path.expanduser(tokenFileName.replace("$HOME", home))
        self._api = ApiClient(self, raw)

    def login(self):
        if super().is_token_valid() is True:
            return

        if super().get_token() is None and os.path.exists(self._tokenFileName):            
            with open(self._tokenFileName, "r") as tokenFile:
                self.token = json.load(tokenFile)

            if self._raw: print("--- token read")
            super().set_token(self.token)

        state = super().login()

        if self._raw: print("--- authentication state: " + state)

        if state != "Valid":
            self.token = super().get_token()
            
            with open(self._tokenFileName, "w") as tokenFile:
                json.dump(self.token, tokenFile, indent=4)

            if self._raw: print("--- token written")

    def logout(self):
        super().logout()

    def execute_post(self,
                     url,
                     json_data,
                     function_description,
                     expected_status_code):
        return super().execute_post(url, json_data, function_description, expected_status_code)

    def execute_get(self, url, function_description, expected_status_code):
        return super().execute_get(url, function_description, expected_status_code)

    def get_devices(self, group=None):
        return self._api.get_devices()

    def dump(self, id):
        return self._api.dump(id)

    def history(self, id, mode, date, tz="+01:00"):
        return self._api.history(id, mode, date, tz)

    def get_device(self, id):
        return self._api.get_device(id)

    def set_device(self, id, **kwargs):
        return self._api.set_device(id, **kwargs)
