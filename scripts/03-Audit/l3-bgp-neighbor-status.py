#---------------------------------------------------------------------------------------------------------------
# DESCRIPTION:
# This script connects to each device (it has the list of devices from a yaml file) and prints some details about the BGP connections.
# it also write the same ouput on a file (junos-python-l3-bgp-state.log)
#
# AUTHOR:   Khelil SATOR (ksator@juniper.net) / Thomas Grimonet (tgrimonet@juniper.net)
# FILE:     l3-bgp-neighbor-status.py
# CREATED:  2015-11-12
# VERSION: 	1.1
#
# USAGE:
# python l3-bgp-neighbor-status.py -u root -p ****
#
# --------------------------------------------------------------------
#
# HELP: 
# usage: l3-bgp-neighbor-status.py [-h] [-u USERNAME] [-p PASSWORD] [-l LAB]
#
# Python & Junos demo -- version 1.1
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -u USERNAME, --username USERNAME
#                         Username required to connect to devices
#   -p PASSWORD, --password PASSWORD
#                         User password to connect to devices
#   -l LAB, --lab LAB     Files containing device IP address
#
# --------------------------------------------------------------------
#
# Output sample:
# python l3-bgp-neighbor-status.py -u root -p Juniper123
#   * Start checking router 172.30.108.228
#     - INTERNAL BGP neighbor 10.30.1.1 / ESTABLISHED (flap count is: 2)
#     - INTERNAL BGP neighbor 10.30.1.2 / ESTABLISHED (flap count is: 3)
#     - EXTERNAL BGP neighbor 192.168.0.1 / ESTABLISHED (flap count is: 3)
#     - EXTERNAL BGP neighbor 192.168.0.3 / ESTABLISHED (flap count is: 0)
#   * Start checking router 172.30.108.229
#     - INTERNAL BGP neighbor 10.30.1.1 / ESTABLISHED (flap count is: 7)
#     - INTERNAL BGP neighbor 10.30.1.2 / ESTABLISHED (flap count is: 6)
#     - EXTERNAL BGP neighbor 192.168.0.5 / ESTABLISHED (flap count is: 8)
#     - EXTERNAL BGP neighbor 192.168.0.7 / ESTABLISHED (flap count is: 5)
#
# ---------------------------------------------------------------------------------------------------------------

import yaml
from op.bgp import *
from jnpr.junos import Device
from datetime import datetime
import logging
import sys
import argparse
from optparse import OptionParser
from logging.handlers import RotatingFileHandler
import re


### Function to connect to device and then collect data from PhyPort Table
def get_data(router, options ):
	jdev = Device(host=router, user=options.username, password=options.password)
	jdev.open()
	data = BGPNeighborTableJNPR(jdev).get()
	return data

### Function to remove TCP port used in a BGP neighbor information: 192.168.0.15+53904
def stripbgp(data):
    p = re.compile(r'\+\d+')
    return p.sub('', data)

def main(options):

	### Open list of devices
	my_list_of_devices=open(options.lab).read()
	my_list_of_routers=yaml.load(my_list_of_devices)

	for router in my_list_of_routers:
		print "  * Start checking router "+ router
		logger.info("Analyzing router %s",router)
		data = get_data(router,options)
		for item in data:
			print "    - " + item.type.upper() + " BGP neighbor " + stripbgp(item.neighbor) + " / " + item.state.upper() + " (flap count is: " + item.flap_count +")" 
			logger.info("%s BGP neighbor %s / %s (flap count: %s)",item.type.upper() , stripbgp(item.neighbor) , item.state.upper() , item.flap_count)
		logger.info("End of analyzing router %s",router)

# ----------------------------------------------------------------- #
# MAIN Section
# ----------------------------------------------------------------- #

if __name__ == "__main__":
	
	# Default Username and Password. Could be updated through CLI Parameters
	version = "1.1"
	gUser='root'
	gPass='****'
	gFile='../lab-poc.yml'

	### CLI Option parser:
	parser = argparse.ArgumentParser(description="Python & Junos demo -- version "+version)
	parser.add_argument('-u','--username' ,help='Username required to connect to devices',default=gUser)
	parser.add_argument('-p','--password' ,help='User password to connect to devices',default=gPass)
	parser.add_argument('-l','--lab' ,help='Files containing device IP address',default=gFile)
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
	file_handler = logging.FileHandler("junos-python-l3-bgp-state.log")
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	### Add handler to logger
	logger.addHandler(steam_handler)
	logger.addHandler(file_handler)
	logger.info('Start to analyze routers')

	main(options)