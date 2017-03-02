import yaml
from op.commit import *
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
	data = CommitTableJNPR(jdev).get()
	return data

def main(options):

	### Open list of devices
	my_list_of_devices=open(options.lab).read()
	my_list_of_routers=yaml.load(my_list_of_devices)

	for router in my_list_of_routers:
		cli = 0
		netconf = 0
		print "  * Start checking router "+ router
		logger.info("Analyzing router %s",router)
		data = get_data(router,options)
		for item in data:
			if item.commit_method == "cli" :
				cli += 1
			elif item.commit_method == "netconf":
				netconf += 1
            print "    - Number of NETCONF commit: "+ str(netconf)
            global_netconf += netconf
            print "    - Number of CLI commit: "+ str(cli)
            global_cli += cli
    print "\n----------------------------------------"
    print "* # of NETCONF commit: "+str(global_netconf)
    print "* # of CLI commit: "+str(global_cli)
    print "----------------------------------------\n"
# ----------------------------------------------------------------- #
# MAIN Section
# ----------------------------------------------------------------- #

if __name__ == "__main__":

	# Default Username and Password. Could be updated through CLI Parameters
	version = "1.1"
	gUser='root'
	gPass='Poclab123'
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
	file_handler = logging.FileHandler("junos-python-l4-commit-state.log")
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	### Add handler to logger
	logger.addHandler(steam_handler)
	logger.addHandler(file_handler)
	logger.info('Start to analyze routers')

	main(options)
