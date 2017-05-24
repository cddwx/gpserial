#!/usr/bin/env python
# coding=utf-8

import sys
from smcsc_command_direct import smcsc_command_direct

parameter_converter = smcsc_command_direct()


try:
    print parameter_converter.convert(sys.argv[1:])

except Exception as e:
    print "[Error   ] ", e

else:
    pass
