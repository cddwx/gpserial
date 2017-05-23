#!/usr/bin/env python
# coding=utf-8

import sys
from smcsc_command_direct import smcsc_command_direct

parameter_converter = smcsc_command_direct()


#print sys.argv[1:]
print parameter_converter.convert(sys.argv[1:])