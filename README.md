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

Some details are available at the following [page](https://github.com/titom73/junos-py-demo/wiki/Setup-Guide) to correctly setup environment and check all dependencies are installed.

### Create LAB description

All scripts will use the same dictionnary file to list devices involved in this LAB / POC. This file is located under script directory and named `scripts/lab-poc.yml`. Below is an example of the content and should be changed according your setup:

```yaml
--- 
   - 172.30.108.228
   - 172.30.108.229
   - 172.30.108.230
   - 172.30.108.232
   - 172.30.108.233
   - 172.30.108.234
   - 172.30.108.236
```

An example is available at the following [page](https://github.com/titom73/junos-py-demo/blob/master/scripts/lab-poc.yml)

## Script usage
All scripts are using an option to let you change this name (check option -l for each script)

All scripts use parameters to ensure they can match your environment. They have at least following options:
- `--username | -u`: set username used for opening connection on devices
- `--password | -p`: set password used for opening connection on devices

To list all options available for each script, you can use `--help` or `-h` trigger to display help.

Scripts will work at 3 different steps of network life:
- Build: details of these scripts are available [here](https://github.com/titom73/junos-py-demo/wiki/Build-Phase)
- Run: details of these scripts are available [here](https://github.com/titom73/junos-py-demo/wiki/Run-Phase)
- Audit: details of these scripts are available [here](https://github.com/titom73/junos-py-demo/wiki/Audit-Phase)

##Contributing

- Fork it
- Create your feature branch (git checkout -b my-new-feature)
- Commit your changes (git commit -am 'Add some feature')
- Push to the branch (git push origin my-new-feature)
- Create new Pull Request

##Author
Thomas Grimonet / Juniper Networks / [Twitter](https://www.twitter.com/titom73)
Khelil Sator / Juniper Networks