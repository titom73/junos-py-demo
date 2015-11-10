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

3.  optparse Module
```shell
pip install optparse
```

4.  YAML Module
```shell
pip install yaml
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

### Create LAB description

All scripts will use the same dictionnary file to list devices involved in this LAB / POC. This file is located under script directory and named lab-poc.yml. Below is an example of the content and should be changed according your setup:

```
--- 
### List all IPs involved in the POC / Demo
   - 172.30.108.228
   - 172.30.108.229
   - 172.30.108.230
   - 172.30.108.232
   - 172.30.108.233
   - 172.30.108.234
   - 172.30.108.236
```

All scripts are using an option to let you change this name (check option -l for each script)

## Execute Scripts
### Audit phase
#### Check UPLINK and DOWNLINK status
This script connects to each device (it has the list of devices from a yaml file) and prints some details about the UPLINKS and DOWNLINKS accross the whole fabric.

* USAGE:
```python
python l1-check-uplink-status.py -u root -p **** 
```

* Output sample:
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

#### Check UPLINK and DOWNLINK status with flapping information


* USAGE:
```python
python l1-check-flap-interfaces.py -u root -p **** 
```

* Output sample:
```
* Start checking router 172.30.108.228
* Start checking router 172.30.108.229
* Start checking router 172.30.108.230
* Start checking router 172.30.108.232
  - xe-0/0/0:0 (UPLINK - S1 to F1 - 192.168.0.12/31) current status is UP  (last flap: 2015-11-06 12:17:51 UTC (4d 06:00 ago))
  - xe-0/0/2:0 (UPLINK - S1 to F2 - 192.168.0.16/31) current status is UP  (last flap: 2015-11-06 12:17:51 UTC (4d 06:00 ago))
* Start checking router 172.30.108.233
  - xe-0/0/0:0 (UPLINK - S2 to F1 - 192.168.0.14/31) current status is UP  (last flap: 2015-11-06 12:02:18 UTC (4d 06:16 ago))
  - xe-0/0/2:0 (UPLINK - S2 to F2 - 192.168.0.18/31) current status is UP  (last flap: 2015-11-06 11:38:07 UTC (4d 06:40 ago))
* Start checking router 172.30.108.234
  - xe-2/0/0 (DOWNLINK to spine01) current status is UP  (last flap: 2015-11-06 12:17:44 UTC (4d 06:00 ago))
  - xe-2/0/1 (DOWNLINK to spine02) current status is UP  (last flap: 2015-11-06 12:02:08 UTC (4d 06:16 ago))
* Start checking router 172.30.108.236
  - xe-2/0/0 (DOWNLINK to spine01) current status is UP  (last flap: 2015-11-06 12:17:41 UTC (4d 06:00 ago))
  - xe-2/0/1 (DOWNLINK to spine02) current status is UP  (last flap: 2015-11-06 11:37:53 UTC (4d 06:40 ago))
```

