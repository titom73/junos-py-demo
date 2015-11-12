#---------------------------------------------------------------------------------------------------------------
# DESCRIPTION:
# Script to Parse all Python scripts in your script directory to highliht all modules you need to setup your environment
# Output should be added to the check_env.py script
#
# AUTHOR:   Thomas Grimonet (tgrimonet@juniper.net)
# FILE:     create-list-modules.py
# CREATED:  2015-11-12
# VERSION: 	1.0
#
# USAGE:
# python create-list-modules.py  
#---------------------------------------------------------------------------------------------------------------
import sys
import re
import glob

### Array with all modules found
modules = []

### Search for module name
def search(line):
	match = re.search('^(import|from)\s+(\w+)',line)
	if match:
		#print line
		print "  -> "+match.group(2)
		modules.append(match.group(2))

### ----------------------------------------------- ###
#				MAIN Section 						  #
### ----------------------------------------------- ###

### List filename located under the root directory
for filename in glob.iglob('**/*.py'):
	print(filename)
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
### Print all required modules
print 'List of required modules: '
for entry in unique:
	# We want to remove OP because it is a local module and do not require an install
	if entry != "op":
		print '* ', entry
	else:
		unique.remove(entry)

print 'Array to add in check_env script: '
print unique