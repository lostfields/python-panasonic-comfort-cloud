'''
Panasonic session, using Panasonic Comfort Cloud app api
'''

import json
import requests
from . import urls
import os

def _validate_response(response):
    """ Verify that response is OK """
    if response.status_code == 200:
        return
    raise ResponseError(response.status_code, response.text)


class Error(Exception):
    ''' Panasonic session error '''
    pass

class RequestError(Error):
    ''' Wrapped requests.exceptions.RequestException '''
    pass


class LoginError(Error):
    ''' Login failed '''
    pass

class ResponseError(Error):
    ''' Unexcpected response '''
    def __init__(self, status_code, text):
        super(ResponseError, self).__init__(
            'Invalid response'
            ', status code: {0} - Data: {1}'.format(
                status_code,
                text))
        self.status_code = status_code
        self.text = json.loads(text)


class Session(object):
    """ Verisure app session
    
    Args:
        username (str): Username used to login to verisure app
        password (str): Password used to login to verisure app
    
    """

    def __init__(self, username, password, tokenFileName='~/.panasonic-token'):
        self._username = username
        self._password = password
        self._tokenFileName = os.path.expanduser(tokenFileName)
        self._vid = None
        self._groups = None

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        """ If of interest, add exception handler """

    def login(self):
        """ Login to verisure app api """

        if os.path.exists(self._tokenFileName):
            with open(self._tokenFileName, 'r') as cookieFile:
                self._vid = cookieFile.read().strip()

            try:
                self._get_groups()

            except ResponseError:
                self._vid = None
                os.remove(self._tokenFileName)

        if self._vid is None:
            self._create_token()
            with open(self._tokenFileName, 'w') as tokenFile:
                tokenFile.write(self._vid)

            self._get_groups()

    def logout(self):
        """ Logout """

    def _headers(self):
        return {
            "X-APP-TYPE": "1",
            "X-APP-VERSION": "2.0.0",
            "X-User-Authorization": self._vid,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _create_token(self): 
        response = None

        payload = '''{
            "language": "0",
            "loginId": "{username}",
            "password": "{password}"
        }'''.format(username=self._username, password=self._password)

        try:
            response = requests.post(urls.login(), payload, headers=self._headers())
            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)
        
        except requests.exceptions.RequestException as ex:
            raise LoginError(ex)

        _validate_response(response)
        self._vid = json.loads(response.text)['uToken']

    def _get_groups(self):
        """ Get information about groups """
        response = None

        try:
            response = requests.get(urls.get_groups(),headers=self._headers())
            
            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)
        
        except requests.exceptions.RequestException as ex:
            raise RequestError(ex)

        _validate_response(response)
        self._groups = json.loads(response.text)

    def get_device_overview(self, deviceGuid):
        """ get device overview """
        print('Not implemented')