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
#   * jnpr is installed
#   * sys is installed
#   * pip is installed
#   * logging is installed
#   * datetime is installed
#   * argparse is installed
#   * optparse is installed
#   * egg is MISSING (use pip install egg)
# ---------------------------------------------------------------------------------------------------------------

import imp
modules = ['pip','jnpr', 'sys', 'pip', 'logging', 'datetime', 'argparse', 'optparse','yaml']
STATE = True

### def to print status and information message to user
def print_status(module, state):
	if state == True:
		print "  * "+module+" is installed"
	else:
		print "  * "+module+" is MISSING (use pip install "+module+")"

### Parse all modules listed in MODULES disctionary
for module in modules:
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