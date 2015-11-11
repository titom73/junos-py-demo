#---------------------------------------------------------------------------------------------------------------
# DESCRIPTION:
# This script prints the lldp neighbors of the whole fabric.
# it connects to each device (it has the list of devices from a yaml file) and get the lldp neighbors of each device and print some details regarding this.
# it also write the same ouput on a file (junos-python-l2-lldp-status.log)
#
# AUTHOR:   Khelil SATOR (ksator@juniper.net) / Thomas Grimonet (tgrimonet@juniper.net)
# FILE:     l2-lldp-neighbor-status.py
# CREATED:  2015-11-11
# VERSION: 	1.1
#
# USAGE:
# python l2-lldp-neighbor-status.py -u root -p ****
#
# --------------------------------------------------------------------
#
# HELP: 
#usage: l2-lldp-neighbor-status.py [-h] [-u USERNAME] [-p PASSWORD] [-l LAB]
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
#  * Start checking router 172.30.108.228
#     * Interface et-0/0/50 connected to SPINE02 (DOWNLINK - L1 to S2 - 192.168.0.2/31)
#     * Interface et-0/0/48 connected to SPINE01 (DOWNLINK - L1 to S1 - 192.168.0.0/31)
#     * Interface xe-0/0/6 connected to FR-EX3300-1-133 (uplink to L1)
#     * Interface xe-0/0/7 connected to FR-EX3300-1-133 (ge-0/0/7.0)
#   * Start checking router 172.30.108.229
#     * Interface et-0/0/50 connected to SPINE02 (DOWNLINK - L2 to S2 - 192.168.0.6/31)
#     * Interface et-0/0/48 connected to SPINE01 (DOWNLINK - L2 to S1 - 192.168.0.4/31)
#     * Interface xe-0/0/12 connected to FR-EX3300-1-133 (uplink to L2)
#     * Interface xe-0/0/13 connected to FR-EX3300-1-133 (ge-0/0/13.0)
#   * Start checking router 172.30.108.230
#     * Interface et-0/0/1 connected to SPINE02 (DOWNLINK - L3 to S2 - 192.168.0.10/31)
#     * Interface et-0/0/0 connected to SPINE01 (DOWNLINK - L3 to S1 - 192.168.0.8/31)
#   * Start checking router 172.30.108.232
#     * Interface et-0/0/14 connected to LEAF04 (UPLINK - L4 to S1 - 192.168.0.20/31)
#     * Interface et-0/0/11 connected to LEAF01 (UPLINK - L1 to S1 - 192.168.0.0/31)
#     * Interface et-0/0/12 connected to LEAF02 (UPLINK - L2 to S1 - 192.168.0.4/31)
#     * Interface xe-0/0/2:0 connected to MX-F2-RE0 (DOWNLINK to spine01)
#     * Interface et-0/0/13 connected to LEAF03 (UPLINK - L3 to S1 - 192.168.0.8/31)
#   * Start checking router 172.30.108.233
#     * Interface et-0/0/14 connected to LEAF04 (UPLINK - L4 to S2 - 192.168.0.22/31)
#     * Interface et-0/0/11 connected to LEAF01 (UPLINK - L1 to S2 - 192.168.0.2/31)
#     * Interface et-0/0/12 connected to LEAF02 (UPLINK - L2 to S2 - 192.168.0.6/31)
#     * Interface xe-0/0/2:0 connected to MX-F2-RE0 (DOWNLINK to spine02)
#     * Interface et-0/0/13 connected to LEAF03 (UPLINK - L3 to S2 - 192.168.0.10/31)
#   * Start checking router 172.30.108.234
#     * Interface fxp0 connected to LAB-EX-VC-BACKBONE
#   * Start checking router 172.30.108.236
#     * Interface fxp0 connected to LAB-EX-VC-BACKBONE
#     * Interface xe-2/0/1 connected to SPINE02
#     * Interface xe-2/0/0 connected to SPINE01
#
# --------------------------------------------------------------------

import yaml
# Custom LLDP table seated in script/03-Audit/OP/ directory from this GIT repository 
from op.lldp import LLDPNeighborTableJNPR
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
	data = LLDPNeighborTableJNPR(jdev).get()
	return data

def main(options):

	### Open list of devices
	my_list_of_devices=open(options.lab).read()
	my_list_of_routers=yaml.load(my_list_of_devices)

	for router in my_list_of_routers:
		print "  * Start checking router "+ router
		logger.info("Analyzing router %s",router)
		lldp_neighbors = get_data(router,options)
		for item in lldp_neighbors:
			# Avoid issue due to lack of interface description field returned by LLDP neighbor
			# If description field is not null, then we can use it in our output
			if item.remote_port_desc is not None:
				print "    * Interface " + item.local_int + " connected to " + item.remote_sysname.upper() + " (" + item.remote_port_desc +")" 
				logger.debug("Interface %s connected to %s (%s)" , item.local_int, item.remote_sysname.upper(), item.remote_port_desc)
			# Else we do not call this variable
			else:
				print "    * Interface " + item.local_int + " connected to " + item.remote_sysname.upper()
				logger.debug("Interface %s connected to %s" , item.local_int, item.remote_sysname.upper())
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
	file_handler = logging.FileHandler("junos-python-l2-lldp-status.log")
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	### Add handler to logger
	logger.addHandler(steam_handler)
	logger.addHandler(file_handler)
	logger.info('Start to analyze routers')

	main(options)