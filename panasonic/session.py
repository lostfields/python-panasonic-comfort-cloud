'''
Panasonic session, using Panasonic Comfort Cloud app api
'''

import json
import requests
from . import urls
from . import constants
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
        self._devices = None
        self._deviceIndexer = {}
        self._verifySsl = False

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        
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

        payload = {
            "language": "0",
            "loginId": self._username,
            "password": self._password
        }

        try:
            response = requests.post(urls.login(), json=payload, headers=self._headers(), verify=self._verifySsl)
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
            response = requests.get(urls.get_groups(),headers=self._headers(), verify=self._verifySsl)

            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)
        
        except requests.exceptions.RequestException as ex:
            raise RequestError(ex)

        _validate_response(response)
        self._groups = json.loads(response.text)
        self._devices = None

    def get_devices(self, group=None):
        if self._vid is None:
            self.login()

        if self._devices is None:
            self._devices = []

            for group in self._groups['groupList']:
                for device in group['deviceIdList']:
                    self._deviceIndexer[device['deviceHashGuid']] = device['deviceGuid']
                    
                    self._devices.append({
                        'id': device['deviceHashGuid'],
                        'name': device['deviceName'],
                        'group': group['groupName'],
                        'model': device['deviceModuleNumber']
                    })

        return self._devices

    def get_device(self, id):
        deviceGuid = self._deviceIndexer.get(id)

        if(deviceGuid):
            response = None
            
            try:
                response = requests.get(urls.overview(deviceGuid), headers=self._headers(), verify=self._verifySsl)

                if 2 != response.status_code // 100:
                    raise ResponseError(response.status_code, response.text)
            
            except requests.exceptions.RequestException as ex:
                raise RequestError(ex)

            _validate_response(response)
            _json = json.loads(response.text)
          
            return {
                'id': id,
                'parameters': self._read_parameters(_json['parameters'])
            }

        return None

    def set_device(self, id, **kwargs):
        """ Set parameters of device
        
        Args:
            id  (str): Id of the device
            kwargs   : {temperature=float}, {mode=OperationMode}, {fanSpeed=FanSpeed}, {power=Power}, {AirSwingHorizontal=}, {AirSwingVertical=}, {Eco=EcoMode}
        """

        parameters = {}
        airX = None
        airY = None

        if kwargs is not None:
            for key, value in kwargs.items():
                if key == 'temperature':
                    parameters['temperatureSet'] = value

                if key == 'mode' and isinstance(value, constants.OperationMode):
                    parameters['operationMode'] = value.value

                if key == 'fanSpeed' and isinstance(value, constants.FanSpeed):
                    parameters['fanSpeed'] = value.value

                if key == 'airSwingHorizontal' and isinstance(value, constants.AirSwingLR):
                    airX = value

                if key == 'airSwingVertical' and isinstance(value, constants.AirSwingUD):
                    airY = value


        if airX and airY and airX.value == -1 and airY.value == -1:
            parameters['fanAutoMode'] = constants.AirSwingAutoMode.Both
        elif airX and airX.value == -1:
            parameters['fanAutoMode'] = constants.AirSwingAutoMode.AirSwingLR
        elif airY and airY.value == -1:
            parameters['fanAutoMode'] = constants.AirSwingAutoMode.AirSwingUD
        elif airX and airY:
            parameters['fanAutoMode'] = constants.AirSwingAutoMode.Disabled
    
        if airX is not None and airX.value is not -1:
            parameters['airSwingLR'] = airX.value 

        if airY is not None and airY.value is not -1:
            parameters['airSwingUD'] = airY.value

        print("going to write parameters to {}".format(id))
        print(parameters)

    def _read_parameters(self, parameters = {}):
        value = {}

        if 'operate' in parameters:
            value['power'] = constants.Power(parameters['operate'])

        if 'temperatureSet' in parameters:
            value['temperature'] = parameters['temperatureSet']

        if 'operationMode' in parameters:
            value['mode'] = constants.OperationMode(parameters['operationMode'])
            
        if 'fanSpeed' in parameters:
            value['fanSpeed'] = constants.FanSpeed(parameters['fanSpeed'])

        if 'airSwingLR' in parameters:
            value['airSwingHorizontal'] = constants.AirSwingLR(parameters['airSwingLR'])

        if 'airSwingUD' in parameters:
            value['airSwingVertical'] = constants.AirSwingUD(parameters['airSwingUD'])

        if 'ecoMode' in parameters:
            value['eco'] = constants.EcoMode(parameters['ecoMode'])
        
        if 'fanAutoMode' in parameters:
            if parameters['fanAutoMode'] == constants.AirSwingAutoMode.Both.value:
                value['airSwingHorizontal'] = constants.AirSwingLR.Auto
                value['airSwingVertical'] = constants.AirSwingUD.Auto
            elif parameters['fanAutoMode'] == constants.AirSwingAutoMode.AirSwingLR.value:
                value['airSwingHorizontal'] = constants.AirSwingLR.Auto
            elif parameters['fanAutoMode'] == constants.AirSwingAutoMode.AirSwingUD.value:
                value['airSwingVertical'] = constants.AirSwingUD.Auto

        return value       
