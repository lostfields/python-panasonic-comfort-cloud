## Command line usage

```
usage: comfortcloud.py [-h] [-t TOKEN] username password {list,get,set} ...

Read or change status of Panasonic Climate devices

positional arguments:
  username              Username for Panasonic Comfort Cloud
  password              Password for Panasonic Comfort Cloud
  {list,get,set}        commands
    list                Get a list of all devices
    get                 Get status of a device
    set                 Set status of a device

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        File to store token in
```

```
usage: comfortcloud.py username password get [-h] device

positional arguments:
  device      device number

optional arguments:
  -h, --help  show this help message and exit
```

```
usage: comfortcloud.py username password set [-h] 
                                             [-p, --power {On,Off}]
                                             [-t, --temperature TEMPERATURE]
                                             [-s, --fanspeed {Auto,Low,LowMid,Mid,HighMid,High}]
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
  -s, --fanspeed {Auto,Low,LowMid,Mid,HighMid,High}
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