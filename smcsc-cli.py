#!/usr/bin/env python
# coding=utf-8

import sys

from command_converter import command_converter

converter = command_converter()

#print sys.argv[1:]
try:
    print converter.convert(sys.argv[1:])
    print sys.argv[1:]

except Exception, e:
    print "[Error   ]" , e

else:
    pass
