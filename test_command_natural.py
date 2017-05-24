#!/usr/bin/env python
# coding=utf-8

import sys
from smcsc_command_natural import smcsc_command_natural

parameter_converter = smcsc_command_natural()

# 代码生成测试

commands = [
        [u"1.557 um/step, 向下，1000 um/s(1.6 ms/step)，800 um(514 step)", "08 FF 00 00 02 05 00 01 02 08 04 00 00 01 05 00 01 02 00 00 00", "VD", "1.557", "0", "1000", "800"],
        [u"2.4 um/step, 向下，1500 um/s(1.6 ms/step)，800 um(333 step)", "08 FF 00 00 01 05 00 01 02 08 4E 00 00 01 05 00 01 02 00 00 00", "VD", "2.4", "0", "1500", "800"],
        [u"1.557 um/step, 向上，1000 um/s(1.6 ms/step)，800 um(514 step)", "F8 FF 00 00 02 05 00 01 02 F8 04 00 00 01 05 00 01 02 00 00 00", "VD", "1.557", "1", "1000", "800"],
        [u"1.557 um/step, 向下，649 um/s(2.4 ms/step)，800 um(514 step)", "0C FF 00 00 02 05 00 01 02 0C 04 00 00 01 05 00 01 02 00 00 00", "VD", "1.557", "0", "649", "800"],
        [u"1.557 um/step, 向下，1000 um/s(1.6 ms/step)，195 um(125 step)", "08 7D 00 00 01 05 00 01 02 00 00 00", "VD", "1.557", "0", "1000", "195"],
        [u"1.557 um/step, 向下，389 um/s(4 ms/step)，195 um(125 step)", "05 01 00 03 7D 05 00 01 02 00 00 00", "VD", "1.557", "0", "389", "195"],
        [u"1.557 um/step, 向下，0.00022243 um/s(7000 ms/step)，195 um(125 step)", "05 01 1B 57 7D 05 00 01 02 00 00 00", "VD", "1.557", "0", "0.22243", "195"],

        [u"DELAY, 65530 ms", "05 00 FF FA 01 05 00 01 02 00 00 00", "DELAY", "65530"],
        [u"DELAY, 131070 ms", "05 00 FF FF 02 05 00 01 02 00 00 00", "DELAY", "131070"],
        [u"DELAY, 100000 ms", "05 00 FF FF 01 05 00 01 02 05 00 86 A1 01 05 00 01 02 00 00 00", "DELAY", "100000"],

        [u"ALT, 1.557 um/step，向下，1557 um/s(1 ms/step)，39 um(25 step)，10000 ms，50 次", "05 19 27 10 32 05 00 01 02 00 00 00", "ALT", "1.557", "0", "1557", "39", "10000", "50"],
        [u"ALT, 2.4 um/step，向下，2400 um/s(1 ms/step)，60 um(25 step)，10000 ms，50 次", "05 19 27 10 32 05 00 01 02 00 00 00", "ALT", "2.4", "0", "2400", "60", "10000", "50"],
        [u"ALT, 1.557 um/step，向上，1557 um/s(1 ms/step)，39 um(25 step)，10000 ms，50 次", "F5 19 27 10 32 05 00 01 02 00 00 00", "ALT", "1.557", "1", "1557", "39", "10000", "50"],
        [u"ALT, 1.557 um/step，向下，649 um/s(2.4 ms/step)，39 um(25 step)，10000 ms，50 次", "0C 19 27 10 32 05 00 01 02 00 00 00", "ALT", "1.557", "0", "1557", "39", "10000", "50"],
        [u"ALT, 1.557 um/step，向下，1557 um/s(1 ms/step)，78 um(50 step)，10000 ms，50 次", "05 32 27 10 32 05 00 01 02 00 00 00", "ALT", "1.557", "0", "1557", "78", "10000", "50"],
        [u"ALT, 1.557 um/step，向下，1557 um/s(1 ms/step)，39 um(25 step)，8000 ms，50 次", "05 19 1F 40 32 05 00 01 02 00 00 00", "ALT", "1.557", "0", "1557", "39", "8000", "50"],
        [u"ALT, 1.557 um/step，向下，1557 um/s(1 ms/step)，39 um(25 step)，10000 ms，100 次", "05 19 27 10 64 05 00 01 02 00 00 00", "ALT", "1.557", "0", "1557", "39", "10000", "100"],
        ]

for command in commands:
    print command[0]
    print command[1]
    try:
        print " ".join(parameter_converter.convert(command[2:])) + " (" + " ".join(command[2:]) + ")"
    except Exception, e:
        print "[Error   ] ", e
    else:
        pass
    print ""

# 命令错误检查测试

error_check_commands = [
        ["Empty command"],

        ["Unknown command", "ddd"],

        ["Parameter number wrong", "VD"],
        ["Parameter number wrong", "VD", "1"],
        ["Parameter number wrong", "VD", "1", "2", "3", "4", "5"],
        ["Step wrong", "VD", "a", "1", "1000", "100"],
        ["Direction wrong", "VD", "1.557", "a", "1000", "100"],
        ["Direction wrong", "VD", "1.557", "-1", "1000", "100"],
        ["Direction wrong", "VD", "1.557", "2", "1000", "100"],
        ["Direction wrong", "VD", "1.557", "1.3", "1000", "100"],
        ["Speed wrong", "VD", "1.557", "1", "a", "100"],
        ["Speed wrong", "VD", "1.557", "1", "0.023", "100"],
        ["Speed wrong", "VD", "1.557", "1", "389.26", "100"],
        ["Speed wrong", "VD", "1.557", "1", "7786", "100"],
        ["Distance wrong", "VD", "1.557", "1", "1000", "a"],
        ["Distance wrong", "VD", "1.557", "1", "1000", "1.3"],
        ["Distance wrong", "VD", "1.557", "1", "300", "-1"],
        ["Distance wrong", "VD", "1.557", "1", "300", "398"],
        ["Distance wrong", "VD", "1.557", "1", "1000", "-1"],
        ["Distance wrong", "VD", "1.557", "1", "1000", "102038"],


        ["Parameter number wrong", "DELAY"],
        ["Parameter number wrong", "DELAY", "1", "2"],
        ["Interval wrong", "DELAY", "a"],
        ["Interval wrong", "DELAY", "1.0"],
        ["Interval wrong", "DELAY", "-1"],
        ["Interval wrong", "DELAY", "16711426"],

        ["Parameter number wrong", "ALT"],
        ["Parameter number wrong", "ALT", "1"],
        ["Parameter number wrong", "ALT", "1", "2", "3", "4", "5", "6", "7"],
        ["Step wrong", "ALT", "a", "1", "1000", "100", "10000", "100"],
        ["Direction wrong", "ALT", "1.557", "a", "1000", "100", "10000", "100"],
        ["Direction wrong", "ALT", "1.557", "-1", "1000", "100", "10000", "100"],
        ["Direction wrong", "ALT", "1.557", "2", "1000", "100", "10000", "100"],
        ["Direction wrong", "ALT", "1.557", "1.3", "1000", "100", "10000", "100"],
        ["Speed wrong", "ALT", "1.557", "1", "a", "100", "10000", "100"],
        ["Speed wrong", "ALT", "1.557", "1", "518", "100", "10000", "100"],
        ["Speed wrong", "ALT", "1.557", "1", "7786", "100", "10000", "100"],
        ["Distance wrong", "ALT", "1.557", "1", "1000", "a", "10000", "100"],
        ["Distance wrong", "ALT", "1.557", "1", "1000", "1.9", "10000", "100"],
        ["Distance wrong", "ALT", "1.557", "1", "1000", "-1", "10000", "100"],
        ["Distance wrong", "ALT", "1.557", "1", "1000", "398", "10000", "100"],
        ["Interval wrong", "ALT", "1.557", "1", "1000", "100", "a", "100"],
        ["Interval wrong", "ALT", "1.557", "1", "1000", "100", "1.0", "100"],
        ["Interval wrong", "ALT", "1.557", "1", "1000", "100", "-1", "100"],
        ["Interval wrong", "ALT", "1.557", "1", "1000", "100", "65536", "100"],
        ["Count wrong", "ALT", "1.557", "1", "1000", "100", "10000", "a"],
        ["Count wrong", "ALT", "1.557", "1", "1000", "100", "10000", "1.4"],
        ["Count wrong", "ALT", "1.557", "1", "1000", "100", "10000", "-1"],
        ["Count wrong", "ALT", "1.557", "1", "1000", "100", "10000", "256"],
        ]


for command in error_check_commands:
    print command[0] + " (" + " ".join(command[1:]) + ")"
    try:
        print parameter_converter.convert(command[1:])
    except Exception, e:
        print "[Error   ] ", e
    else:
        pass
    print ""
