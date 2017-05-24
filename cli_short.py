#!/usr/bin/env python
# coding=utf-8

import sys
from smcsc_command_short import smcsc_command_short

parameter_converter = smcsc_command_short()


#print sys.argv[1:]
if parameter_converter.convert(sys.argv[1:]) != False:
    print parameter_converter.convert(sys.argv[1:])
