#---------------------------------------------------------------------------------------------------------------
# DESCRIPTION:
# Script to check PYTHON environment and check if all dependencies required to run demo scripts are correctly installed on your system
#
# AUTHOR:   Thomas Grimonet (tgrimonet@juniper.net)
# FILE:     check_env.py
# CREATED:  2015-11-10
# VERSION: 	1.0
#
# USAGE:
# python check_env.py  
#
#
# Output sample:
# 
# python check_env.py
# Required Python's modules to run scripts in this repository:
# yaml      : FOUND
# sys       : FOUND
# os        : FOUND
# argparse  : FOUND
# glob      : FOUND
# jinja2    : FOUND
# pprint    : FOUND
# optparse  : FOUND
# jnpr      : FOUND
# datetime  : FOUND
# logging   : FOUND
# op        : MISSING
# re        : FOUND
# ---------------------------------------------------------------------------------------------------------------

import sys
import re
import glob
import imp

# Array to store all modules found in scripts
modules = []
# Global state: is a module missing ? 
#  FALSE: Yes a module is missing / 
#  TRUE: Everything is under control
STATE = True

### def to print status and information message to user
def print_status(module, state):
	if state == True:
		#print "  * "+module+"\t\t: FOUND"
		print "{0:10}: FOUND".format(module)
	else:
		print "{0:10}: MISSING (use pip install)".format(module, module)

### Search for module name
def search(line):
	match = re.search('^(import|from)\s+(\w+)',line)
	if match:
		#print line
		#print "  -> "+match.group(2)
		modules.append(match.group(2))

### ----------------------------------------------- ###
#				MAIN Section 						  #
### ----------------------------------------------- ###

### List filename located under the root directory
for filename in glob.iglob('**/*.py'):
	#print(filename)
	### open and read file content
	f = open(filename, 'r')
	read_data = f.readlines()
	f.close()
	### then send lines to the search function
	for line in read_data:
		search(line)

### Sort array to remove duplicate entries
unique = []
[unique.append(item) for item in modules if item not in unique]
### Remove all local modules
### i.e.: not provided by PIP
for entry in unique:
	# We want to remove OP because it is a local module and do not require an install
	if entry == "op":
		unique.remove(entry)

### Parse all modules listed in MODULES disctionary
print "Required Python's modules to run scripts in this repository: "
for module in unique:
	### Try to find it, if we can load it, then it is a good point
	try:
	    imp.find_module(module)
	    print_status(module,True)
	### Else we have to inform user and change state to false: system is not ready for next step
	except ImportError:
	    STATE = False
	    print_status(module,False)

print ""
### Check if at least one package is missing
if STATE != True:
	print "***********************\n! Please install missing packages before running demo scripts. Otherwise, they won't work\n***********************\n"