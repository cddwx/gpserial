#!/usr/bin/env python
# coding=utf-8

import sys
from smcsc_parameter import smcsc_parameter

parameter_converter = smcsc_parameter()

#print sys.argv[1:]
print parameter_converter.command(sys.argv[1:])
