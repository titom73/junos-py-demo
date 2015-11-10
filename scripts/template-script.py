#---------------------------------------------------------------------------------------------------------------
# DESCRIPTION:
# 
#
# AUTHOR:   Khelil SATOR (ksator@juniper.net) / Thomas Grimonet (tgrimonet@juniper.net)
# FILE:     
# CREATED:  
# VERSION: 	1.1
#
# USAGE:
# 
#
# --------------------------------------------------------------------
#
# HELP: 
#
#
# --------------------------------------------------------------------
#
# Output sample:
#
#
# --------------------------------------------------------------------
# 
# Input Sample (pay attention to the YAML syntax)
#
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


def main(options):

	### Open list of devices
	my_list_of_devices=open(options.lab).read()
	my_list_of_routers=yaml.load(my_list_of_devices)

	for router in my_list_of_routers:
		print "  * Start checking router "+ router
		logger.info("Analyzing router %s",router)
		
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