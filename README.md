# python-panasonic-comfort-cloud
A **Python module** for reading and changing the status of **Panasonic climate devices** through Panasonic Comfort Cloud app API


## Command line usage

```
usage: pcomfortcloud [-h] [-t TOKEN] [-r BOOL] username password {list,get,set,dump,history} ...

Read or change status of Panasonic climate devices

positional arguments:
  username              Username for Panasonic Comfort Cloud
  password              Password for Panasonic Comfort Cloud
  {list,get,set,dump,history}
                        commands
    list                Get a list of all devices
    get                 Get device parameters
    set                 Set device parameter(s)
    dump                Dump all data of a device
    history             Dump history of a device

options:
  -h, --help            show this help message and exit
  -t, --token TOKEN     File to store token in
  -r, --raw BOOL        Raw dump of response
```

Get a list of all devices:
```
usage: pcomfortcloud.py username password list [-h]

options:
  -h, --help  show this help message and exit
```

Get device parameters:
```
usage: pcomfortcloud.py username password get [-h] device

positional arguments:
  device      Device number (e.g., 1, 2, ...)

options:
  -h, --help  show this help message and exit
```

Set device parameter(s):
```
usage: pcomfortcloud.py username password set [-h]
                                              [-p, --power {On,Off}]
                                              [-t, --temperature TEMPERATURE]
                                              [-f, --fanSpeed {Auto,Low,LowMid,Mid,HighMid,High}]
                                              [-m, --mode {Auto,Cool,Dry,Heat,Fan}]
                                              [-e, --eco {Auto,Quiet,Powerful}]
                                              [-n, --nanoe {On,Off,ModeG,All}]
                                              [-y, --airSwingVertical {Auto,Down,DownMid,Mid,UpMid,Up}]
                                              [-x, --airSwingHorizontal {Auto,Left,LeftMid,Mid,RightMid,Right}]
                                              device

positional arguments:
  device                Device number (e.g., 1, 2, ...)

options:
  -h, --help            show this help message and exit
  -p, --power {On,Off}  Power mode
  -t, --temperature TEMPERATURE
                        Temperature in decimal format
  -f, --fanSpeed {Auto,Low,LowMid,Mid,HighMid,High}
                        Fan speed
  -m, --mode {Auto,Cool,Dry,Heat,Fan}
                        Operation mode
  -e, --eco {Auto,Quiet,Powerful}
                        Eco mode
  -n, --nanoe {On,Off,ModeG,All}
                        Nanoe mode
  -y, --airSwingVertical {Auto,Down,DownMid,Mid,UpMid,Up}
                        Vertical position of the air swing
  -x, --airSwingHorizontal {Auto,Left,LeftMid,Mid,RightMid,Right}
                        Horizontal position of the air swing
```

Dump all data of a device:
```
usage: pcomfortcloud username password dump [-h] device

positional arguments:
  device      Device number (e.g., 1, 2, ...)

optional arguments:
  -h, --help  show this help message and exit
```

Dump history of a device:
```
usage: pcomfortcloud username password history [-h] device mode date

positional arguments:
  device      Device number (e.g., 1, 2, ...)
  mode        Mode (Day, Week, Month, Year)
  date        Date, for example: 20190807

optional arguments:
  -h, --help  show this help message and exit
```

### Command line security warning

Be aware that passing your **username and password** directly as positional arguments can be insecure, as these credentials may be saved in your shell's history file (e.g., `.bash_history`).

For better security, especially in shared or logged environments, it is recommended to:
1.  Use the **token file** option (`-t TOKEN`) after the first successful login.
2.  Use environment variables for sensitive credentials where possible.


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

The package can be found on PyPI: [https://pypi.org/project/pcomfortcloud/](https://pypi.org/project/pcomfortcloud/)

### Installation

Install the module using **pip**:

```bash
pip install pcomfortcloud
```

## Developer info

- `python .\setup.py sdist bdist_wheel`
- `python -m twine upload dist/*`
