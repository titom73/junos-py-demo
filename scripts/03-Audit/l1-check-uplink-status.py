#---------------------------------------------------------------------------------------------------------------
# DESCRIPTION:
# This script connects to each device (it has the list of devices from a yaml file) and prints some details about the UPLINKS and DOWNLINKS accross the whole fabric.
# it also write the same ouput on a file (junos-python-l1.log)
#
# AUTHOR:   Khelil SATOR (ksator@juniper.net) / Thomas Grimonet (tgrimonet@juniper.net)
# FILE:     uplinks_and_downlinks_down.py
# CREATED:  2015-11-10
# VERSION: 	1.1
#
# USAGE:
# python l1-check-uplink-status.py -u root -p **** 
#
# --------------------------------------------------------------------
#
# HELP: 
# usage: l1-check-uplink-status.py [-h] [-u USERNAME] [-p PASSWORD] [-l LAB]
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
#   * Start checking router 172.30.108.228
#	  * Start checking router 172.30.108.229
#	  * Start checking router 172.30.108.230
#	  * Start checking router 172.30.108.232
#	    - Network Interface xe-0/0/0:0(UPLINK - S1 to F1 - 192.168.0.12/31) is UP
#	    - Network Interface xe-0/0/2:0(UPLINK - S1 to F2 - 192.168.0.16/31) is UP
#	  * Start checking router 172.30.108.233
#	    - Network Interface xe-0/0/0:0(UPLINK - S2 to F1 - 192.168.0.14/31) is UP
#	    - Network Interface xe-0/0/2:0(UPLINK - S2 to F2 - 192.168.0.18/31) is UP
#	  * Start checking router 172.30.108.234
#	    - Network Interface xe-2/0/0(DOWNLINK to spine01) is UP
#	    - Network Interface xe-2/0/1(DOWNLINK to spine02) is UP
#	  * Start checking router 172.30.108.236
#	    - Network Interface xe-2/0/0(DOWNLINK to spine01) is UP
#	    - Network Interface xe-2/0/1(DOWNLINK to spine02) is UP
#
# --------------------------------------------------------------------
# 
# Input Sample (pay attention to the YAML syntax)
# --- 
# ### List all IPs involved in the POC / Demo
#    - 172.30.108.228
#    - 172.30.108.229
#    - 172.30.108.230
#    - 172.30.108.232
#    - 172.30.108.233
#    - 172.30.108.234
#    - 172.30.108.236
# ---------------------------------------------------------------------------------------------------------------

import yaml
from jnpr.junos.op.phyport import *
from jnpr.junos import Device
from datetime import datetime
import logging
import sys
import argparse
from optparse import OptionParser
from logging.handlers import RotatingFileHandler

### Function to connect to device and then collect data from PhyPort Table
def get_data(router, options ):
	jdev = Device(host=router, user=options.username, password=options.password)
	jdev.open()
	ports = PhyPortTable(jdev).get()
	return ports

def main(options):

	### Open list of devices
	my_list_of_devices=open(options.lab).read()
	my_list_of_routers=yaml.load(my_list_of_devices)

	for router in my_list_of_routers:
		print "  * Start checking router "+ router
		logger.info("Analyzing router %s",router)
		ports = get_data(router,options)
		for item in ports:
			if item.description:
				if "LINK" in item.description:
					if item.oper == "down":
						logMessage = "    - Network Interface " + item.key + "(" + item.description + ") is DOWN"	
						print (logMessage)
						logger.info(logMessage)
					if item.oper == "up":
						logMessage = "    - Network Interface " + item.key + "(" + item.description + ") is UP"	
						print (logMessage)
						logger.info(logMessage)
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
	file_handler = logging.FileHandler("junos-python-l1.log")
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	### Add handler to logger
	logger.addHandler(steam_handler)
	logger.addHandler(file_handler)
	logger.info('Start to analyze routers')

	main(options)