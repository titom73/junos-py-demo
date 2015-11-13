#---------------------------------------------------------------------------------------------------------------
# DESCRIPTION:
# Script to massively create device configuration  based on a template and with variable datas located in a YAML file
#
# AUTHOR:   Khelil SATOR (ksator@juniper.net) / Thomas Grimonet (tgrimonet@juniper.net)
# FILE:     build-configuration-offline.py
# CREATED:  2015-11-11
# VERSION: 	1.1
#
# USAGE:
# python build-configuration-offline.py -t template-example/ip_fabric_template_for_leaves_build_phase2.j2 -y template-example/ip_fabric_variables_definition_for_leaves_build_phase2.yml -k host_name
#
# --------------------------------------------------------------------
#
# HELP: 
# python build-configuration-offline.py -h
# usage: build-configuration-offline.py [-h] [-y YAML] [-t TEMPLATE] [-b BASE]
#                                       [-k KEY]
#
# Python & Junos demo -- version 1.1
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -y YAML, --yaml YAML  Provides YAML file to fill Jinja2 template,
#                         default=dict.yml
#   -t TEMPLATE, --template TEMPLATE
#                         template file, default=./template.j2
#   -b BASE, --base BASE  Base to construct filename, default=generated-conf-
#   -k KEY, --key KEY     Key used in YAML file, default=hostname
#
# --------------------------------------------------------------------
#
# Output sample:
#python build-configuration-offline.py -t template-example/ip_fabric_template_for_leaves_build_phase2.j2 -y template-example/ip_fabric_variables_definition_for_leaves_build_phase2.yml -k host_name
# Start configuration building
#   - Generate config for leaf1
#
#   - Generate config for leaf2
#
#   - Generate config for leaf3
#
# End of Script
#
# --------------------------------------------------------------------

import yaml
import sys
import os
import argparse
from glob import glob
from jinja2 import Template
from pprint import pprint

version = "1.1"

def display_help():
    print ""

# Manage cmdLine parameters.
parser = argparse.ArgumentParser(description="Python & Junos demo -- version "+version)
parser.add_argument('-y', '--yaml', help='Provides YAML file to fill Jinja2 template, default=dict.yml',default='dict.yml')
parser.add_argument('-t','--template' ,help='template file, default=./template.j2',default='./template.j2')
parser.add_argument('-b','--base' ,help='Base to construct filename, default=generated-conf-',default='generated-conf-')
parser.add_argument('-k','--key' ,help='Key used in YAML file, default=hostname',default='hostname')
# Manage All options and construct array
options = parser.parse_args()


print 'Start configuration building'
# YAML file.
with open( options.yaml ) as fh:
    data = yaml.load( fh.read() )

# Jinja2 template file.
with open( options.template ) as t_fh:
    t_format = t_fh.read()

for device in data:
	hostname = device[ options.key ]
	print '  - Generate config for '+hostname
	print ''
	#pprint( device )
	template = Template( t_format )

	confFile = open( options.base + str(hostname) + '.conf','w')
	confFile.write( template.render( device ) )
	confFile.close()

print 'End of Script'