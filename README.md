# junos-py-demo
Demo Script to demonstrate ability to automate Junos with Python

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

Before running any script, we have to check our system is ready with all dependencies installed:
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

Run Scripts
