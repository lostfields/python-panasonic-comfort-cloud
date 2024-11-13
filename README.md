# python-panasonic-comfort-cloud
A python module for reading and changing status of panasonic climate devices through Panasonic Comfort Cloud app api

## Command line usage

```
usage: pcomfortcloud.py [-h] [-t TOKEN] username password {list,get,set} ...

Read or change status of Panasonic Climate devices

positional arguments:
  username              Username for Panasonic Comfort Cloud
  password              Password for Panasonic Comfort Cloud
  {list,get,set,dump}   commands
    list                Get a list of all devices
    get                 Get status of a device
    set                 Set status of a device
    dump                Dump raw data of a device
    history             Dump history of a device

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        File to store token in
  -a AUTHFILE, --authfile AUTHFILE
                        File to store credentials in (instead of using username and password)
  -s [BOOL], --skipVerify [BOOL]
                        Skip Ssl verification
  -r [BOOL], --raw [BOOL]
                        Raw dump of response
```

```
usage: pcomfortcloud.py username password get [-h] device

positional arguments:
  device      device number

optional arguments:
  -h, --help  show this help message and exit
```

```
usage: pcomfortcloud.py username password set [-h]
                                             [-p, --power {On,Off}]
                                             [-t, --temperature TEMPERATURE]
                                             [-f, --fanspeed {Auto,Low,LowMid,Mid,HighMid,High}]
                                             [-m, --mode {Auto,Cool,Dry,Heat,Fan}]
                                             [-e, --eco {Auto,Quiet,Powerful}]
                                             [-y, --airswingvertical {Auto,Down,DownMid,Mid,UpMid,Up}]
                                             [-x, --airswinghorizontal {Auto,Left,LeftMid,Mid,RightMid,Right}]
                                             device

positional arguments:
  device                Device number

optional arguments:
  -h, --help
                        show this help message and exit
  -p, --power {On,Off}
                        Power mode
  -t, --temperature TEMPERATURE
                        Temperature in decimal format
  -f, --fanspeed {Auto,Low,LowMid,Mid,HighMid,High}
                        Fan speed
  -m, --mode {Auto,Cool,Dry,Heat,Fan}
                        Operation mode
  -e, --eco {Auto,Quiet,Powerful}
                        Eco mode
  -y, --airswingvertical {Auto,Down,DownMid,Mid,UpMid,Up}
                        Vertical position of the air swing
  -x, --airswinghorizontal {Auto,Left,LeftMid,Mid,RightMid,Right}
                        Horizontal position of the air swing
```

```
usage: pcomfortcloud username password dump [-h] device

positional arguments:
  device      Device number 1-x

optional arguments:
  -h, --help  show this help message and exit
```

```
usage: pcomfortcloud username password history [-h] device mode date

positional arguments:
  device      Device number 1-x
  mode        mode (Day, Week, Month, Year)
  date        date of day like 20190807

optional arguments:
  -h, --help  show this help message and exit
```

## Module usage


```python
import pcomfortcloud


session = pcomfortcloud.Session('user@example.com', 'mypassword')
session.login()

client = pcomfortcloud.ApiClient(session)

devices = client.get_devices()

print(devices)

print(client.get_device(devices[0]['id']))

client.set_device(devices[0]['id'],
  power = pcomfortcloud.constants.Power.On,
  temperature = 22.0)
```

## PyPi package
can be found at https://pypi.org/project/pcomfortcloud/

### How to publish package;
- `python .\setup.py sdist bdist_wheel`
- `python -m twine upload dist/*`

## Auth File
Instead of specifying the username and password on the command line, they can optionally, be stored in a YAML file.
To use the auth file, on the command line, set the username to authfile and set the password to the full path of the YAML file 

The format of the auth file is:
```
username: USERNAME
password: PASSWORD
```