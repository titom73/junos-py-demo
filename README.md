# junos-py-demo
Demo Scripts to demonstrate ability to automate Junos with Python

## About
This repository provides some scripts to demonstrate how to automate Junos with Python, So There is 3 different sections:
- Build
- Run
- Audit

All scripts are located under script directory of this repository

## Setup environment:
### Setup Python for windows
Download latest version of Python 2.7 available on Python.org website: https://www.python.org/downloads/windows/

### Install required modules:
In order to execute scripts provided by this repository, you have to install some basic modules from python repository:

1. Junos-py-ez

More documentation available at https://github.com/Juniper/py-junos-eznc

```shell
pip install junos-eznc
```

2.  argparse Module
```shell
pip install argparse
```

2.  optparse Module
```shell
pip install optparse
```

### Check your environment

Before running any script, we have to check if our system is ready to execute scripts with all dependencies installed:
```shell
python check_env.py
  * jnpr is installed
  * sys is installed
  * pip is installed
  * logging is installed
  * datetime is installed
  * argparse is installed
  * optparse is installed
  * egg is MISSING (use pip install egg)
```

## Running Scripts
### Audit phase
#### Check UPLINK and DOWNLINK status
This script connects to each device (it has the list of devices from a yaml file) and prints some details about the UPLINKS and DOWNLINKS accross the whole fabric.

1. USAGE:
```python
python l1-check-uplink-status.py -u root -p **** 
```

2. Output sample:
```
  * Start checking router 172.30.108.228
  * Start checking router 172.30.108.229
  * Start checking router 172.30.108.230
  * Start checking router 172.30.108.232
    - Network Interface xe-0/0/0:0(UPLINK - S1 to F1 - 192.168.0.12/31) is UP
    - Network Interface xe-0/0/2:0(UPLINK - S1 to F2 - 192.168.0.16/31) is UP
  * Start checking router 172.30.108.233
    - Network Interface xe-0/0/0:0(UPLINK - S2 to F1 - 192.168.0.14/31) is UP
    - Network Interface xe-0/0/2:0(UPLINK - S2 to F2 - 192.168.0.18/31) is UP
  * Start checking router 172.30.108.234
    - Network Interface xe-2/0/0(DOWNLINK to spine01) is UP
    - Network Interface xe-2/0/1(DOWNLINK to spine02) is UP
  * Start checking router 172.30.108.236
    - Network Interface xe-2/0/0(DOWNLINK to spine01) is UP
    - Network Interface xe-2/0/1(DOWNLINK to spine02) is UP
```