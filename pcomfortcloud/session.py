from .authentication import Authentication
from .apiclient import ApiClient
from . import constants

class Session(Authentication):
    def __init__(self, username, password, token, raw=False):
        super().__init__(username, password, token, raw)
        
        self._app_version = constants.X_APP_VERSION
        self._update_app_version()

        self._api = ApiClient(self, raw)

    def get_token(self):
        return super().get_token()

    def login(self):
        super().login()

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
