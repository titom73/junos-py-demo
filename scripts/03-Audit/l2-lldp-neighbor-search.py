#---------------------------------------------------------------------------------------------------------------
# DESCRIPTION:
# This script asks you which lldp neighbor you are looking for.
# it searches this lldp neighbor accross the whole ip fabric.
# it connects to each device (it has the list of devices from a yaml file) and get the lldp neighbors and compare them with the one you are looking for.
# if it find it, it indicates where is it.
# it also write the same ouput on a file (junos-python-l2-lldp-search.log)
#
# AUTHOR:   Khelil SATOR (ksator@juniper.net) / Thomas Grimonet (tgrimonet@juniper.net)
# FILE:     l2-lldp-neighbor-search.py
# CREATED:  2015-11-11
# VERSION: 	1.1
#
# USAGE:
# python l2-lldp-neighbor-search.py -u root -p **** -s myHostnameToFind
#
# --------------------------------------------------------------------
#
# HELP: 
#usage: l2-lldp-neighbor-search.py [-h] [-u USERNAME] [-p PASSWORD] [-l LAB]
#                                   [-s SEARCH]
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
#   -s SEARCH, --search SEARCH
#                         Hostname to search in the lab
#
# --------------------------------------------------------------------
#
# # Output sample:
# python l2-lldp-neighbor-search.py -u root -p Juniper123 -s spine01
#   * Start checking router 172.30.108.228
#     * Found it on 172.30.108.228 / et-0/0/48
#   * Start checking router 172.30.108.229
#     * Found it on 172.30.108.229 / et-0/0/48
#   * Start checking router 172.30.108.230
#     * Found it on 172.30.108.230 / et-0/0/0
#   * Start checking router 172.30.108.232
#   * Start checking router 172.30.108.233
#   * Start checking router 172.30.108.234
#   * Start checking router 172.30.108.236
#     * Found it on 172.30.108.236 / xe-2/0/0
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
	found = False 	# Help to remember if we found a connection or not

	for router in my_list_of_routers:
		print "  * Start checking router "+ router
		logger.info("Start checking router %s",router)
		lldp_neighbors = get_data(router,options)
		for item in lldp_neighbors:
			if item.remote_sysname == options.search:
				print "    * Found it on " + router +" / "+item.local_int 
				logger.debug("Interface %s connected to %s (%s)" , item.local_int, item.remote_sysname.upper(), item.remote_port_desc)
				found = True
	if found is not True:
		print "  !! Device is not connected to your lab (or LLDP is not activated on it)"
		logger.warning("Device is not connected to your lab (or LLDP is not activated on it)")
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
	gSearch = "localhost"

	### CLI Option parser:
	parser = argparse.ArgumentParser(description="Python & Junos demo -- version "+version)
	parser.add_argument('-u','--username' ,help='Username required to connect to devices',default=gUser)
	parser.add_argument('-p','--password' ,help='User password to connect to devices',default=gPass)
	parser.add_argument('-l','--lab' ,help='Files containing device IP address',default=gFile)
	parser.add_argument('-s','--search' ,help='Hostname to search in the lab',default=gSearch)
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
	file_handler = logging.FileHandler("junos-python-l2-lldp-search.log")
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	### Add handler to logger
	logger.addHandler(steam_handler)
	logger.addHandler(file_handler)
	logger.info('Start to analyze routers')

	main(options)