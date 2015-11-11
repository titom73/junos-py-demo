#---------------------------------------------------------------------------------------------------------------
# DESCRIPTION:
# Provide a function to upload configuration on multiple devices by using template renderer and data from YAML. For security reason, -s trigger is set to true and no change will be applied on devices: Only a commit / diff and then rollback
# For any change, do not use this trigger
#
# AUTHOR:   Khelil SATOR (ksator@juniper.net) / Thomas Grimonet (tgrimonet@juniper.net)
# FILE:     run-deploy-jinja-template.py
# CREATED:  2015-11-11
# VERSION: 	1.1
#
# USAGE:
# python run-deploy-jinja-template.py -d templates/data.yml -t templates/system.conf -u root -p Juniper123 --safe -v
#
# --------------------------------------------------------------------
#
# HELP: 
# usage: run-deploy-jinja-template.py [-h] [-d DATA] [-t TEMPLATE] [-u USERNAME]
#                                     [-p PASSWORD] [-k KEY] [-v] [-s]
#
# Python & Junos demo -- version 1.1
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -d DATA, --data DATA  YAML file containing data to merge with template
#   -t TEMPLATE, --template TEMPLATE
#                         Path to template file -- default is
#                         ./templates/system.conf
#   -u USERNAME, --username USERNAME
#                         Username required to connect to devices
#   -p PASSWORD, --password PASSWORD
#                         User password to connect to devices
#   -k KEY, --key KEY     Key to identify host in YAML file
#   -v, --verbose         Increase Verbosity
#   -s, --safe            Activate protection against network change -- Use it
#                         in case of dry-run
#
# --------------------------------------------------------------------
#
# Output sample:
# Start configuration building                         
#   * Start updating 172.30.108.228                    
#   * Connected to 172.30.108.228                      
#     * Configuration Diff is :                        
#                                                     
#   [edit system]                                      
#   -  host-name leaf01;                               
#   +  host-name leaf01-automate;                      
#   +  location {                                      
#   +      building ESX01;                             
#   +      floor 4;                                    
#   +  }                                               
#   [edit system name-server]                          
#       8.8.4.4 { ... }                                
#   +   10.73.2.253;                                   
#   [edit snmp]                                        
#   +  description leaf01-automate;                    
#   -  location DC1;                                   
#   +  location "AS73 Exchanger Network";              
#   +  contact "admimn@inetsix.net";                   
#   +  community inetsix-ro {                          
#   +      authorization read-only;                    
#   +  }                                               
#   +  trap-group space {                              
#   +      targets {                                   
#   +          10.1.1.9;                               
#   +      }                                           
#   +  }                                               
#                                                     
#     ** Running in dry-run mode, commit aborted       
#                                                     
# End of Script                                        
#
# --------------------------------------------------------------------
# 
# Input Sample (pay attention to the YAML syntax)
# ---
# - host: 172.30.108.228 
#   hostName: leaf01-automate
# ---------------------------------------------------------------------------------------------------------------

import sys
from optparse import OptionParser
import argparse
import yaml
from jinja2 import Template
from jnpr.junos import Device
from datetime import datetime
import logging
import sys
from logging.handlers import RotatingFileHandler

# Junos Python Libs (py-junos-eznc)
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *

# Default Username and Password. Could be updated through CLI Parameters
gUser='root'
gPass='***'

# Internal do not change
delimiter_line = "**************************************"
delimiter_tab = "  "
version = "1.1"

def display_help():
    print ""

def cleanup_answer(output):
    """
    Def to cleanup device response
    return ARRAY of string, If it is not a String, return Array with 'No Change' inside
    """
    if isinstance(output,str):
        result = output.split("\n")
    else:
        result = [str(output)]
    return result

def main():
    print 'Start configuration building'
    # YAML file.
    with open( options.data ) as fh:
        data = yaml.load( fh.read() )

    # Jinja2 template file.
    with open( options.template ) as t_fh:
        t_format = t_fh.read()

    for device in data:
        hostname = device[ options.key ]
        print '  * Start updating '+hostname
        logger.info('Start updating %s',hostname)
        template = Template( t_format )
        jdev = Device( host=hostname , user=options.username , password=options.password , gather_facts=False)
        jdev.open()
        print "  * Connected to "+ hostname
        logger.info('connected to %s',hostname)
        jdev.bind( cu=Config )
        # Execute Rollback to prevent commit change from old config session
        jdev.cu.rollback()
        rsp = jdev.cu.load( template_path = options.template, template_vars = device)

        # Display some informations - Configuration Diff
        # Only if verbose Mode is enable
        if( options.verbose ):
            print delimiter_tab+"  * Configuration Diff is :"
            for diff in cleanup_answer( jdev.cu.diff() ):
                print delimiter_tab+diff
        # Apply changes if options.safe is not enable. Protect user aginst script error. In case of test, user can emulate script and change w/out impact production
        if options.safe is True:
            print delimiter_tab+'  ** Running in dry-run mode, commit aborted'
            logger.info('Running in DRY-RUN mode, commit aborted and rollback to previsous stage')
            # Execute Rollback to prevent change are loaded and not discraded before next config change
            jdev.cu.rollback()
        else:
            rsp = jdev.cu.commit()
            print delimiter_tab+"  * Commit Complete"
            logger.warning('Dry-run disable, commit complete')
        print ("")

    print 'End of Script'


# Launch Script
if __name__ == "__main__":
	# Manage cmdLine parameters.
	parser = argparse.ArgumentParser(description="Python & Junos demo -- version 1.1")
	parser.add_argument('-d', '--data', help='YAML file containing data to merge with template',default="./templates/data.yml")
	parser.add_argument('-t','--template' ,help='Path to template file -- default is ./templates/system.conf',default="./templates/system.conf")
	parser.add_argument('-u','--username' ,help='Username required to connect to devices',default=gUser)
	parser.add_argument('-p','--password' ,help='User password to connect to devices',default=gPass)
	parser.add_argument('-k','--key' ,help='Key to identify host in YAML file',default='host')
	parser.add_argument('-v','--verbose' ,help='Increase Verbosity',action="store_true")
	parser.add_argument('-s','--safe' ,help='Activate protection against network change -- Use it in case of dry-run',action="store_true")
	# Manage All options and construct array
	options = parser.parse_args()

	### Activate logging to keep trace in log file
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(funcName)s :: %(message)s')
	### Display log with CRITICAL level and higher
	steam_handler = logging.StreamHandler()
	steam_handler.setLevel(logging.CRITICAL)
	steam_handler.setFormatter(formatter)
	logger.addHandler(steam_handler)
	### Write log with DEBUG level and higher
	file_handler = logging.FileHandler("junos-python-deploy-template.log")
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	### Add handler to logger
	logger.addHandler(steam_handler)
	logger.addHandler(file_handler)
	logger.info('Start to analyze routers')

	# Launch script engine
	main()
