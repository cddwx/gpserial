#!/usr/bin/env python
# coding=utf-8

import sys
from smcsc_command_short import smcsc_command_short

parameter_converter = smcsc_command_short()

# 代码生成测试

commands = [
        [u"向下，1 ms/step，125 step", "05 7D 00 00 01 05 00 01 02 00 00 00", "VD", "0", "1", "125"],
        [u"向上，1 ms/step，125 step", "F5 7D 00 00 01 05 00 01 02 00 00 00", "VD", "1", "1", "125"],
        [u"向下，2.6 ms/step，125 step", "0D 7D 00 00 01 05 00 01 02 00 00 00", "VD", "0", "2.6", "125"],
        [u"向下，1 ms/step，510 step", "05 FF 00 00 02 05 00 01 02 00 00 00", "VD", "0", "1", "510"],
        [u"向下，1 ms/step，500 step", "05 FF 00 00 01 05 00 01 02 05 F5 00 00 01 05 00 01 02 00 00 00", "VD", "0", "1", "500"],
        [u"向下，4 ms/step，125 step", "05 01 00 03 7D 05 00 01 02 00 00 00", "VD", "0", "4", "125"],
        [u"向下，65500 ms/step，125 step", "05 01 FF DB 7D 05 00 01 02 00 00 00", "VD", "0", "65500", "125"],

        [u"DELAY, 65530 ms", "05 00 FF FA 01 05 00 01 02 00 00 00", "DELAY", "65530"],
        [u"DELAY, 131070 ms", "05 00 FF FF 02 05 00 01 02 00 00 00", "DELAY", "131070"],
        [u"DELAY, 100000 ms", "05 00 FF FF 01 05 00 01 02 05 00 86 A1 01 05 00 01 02 00 00 00", "DELAY", "100000"],

        [u"ALT, 向下，1 ms/step，25 step，10000 ms，50 次", "05 19 27 10 32 05 00 01 02 00 00 00", "ALT", "0", "1", "25", "10000", "50"],
        [u"ALT, 向上，1 ms/step，25 step，10000 ms，50 次", "F5 19 27 10 32 05 00 01 02 00 00 00", "ALT", "1", "1", "25", "10000", "50"],
        [u"ALT, 向下，2.4 ms/step，25 step，10000 ms，50 次", "0C 19 27 10 32 05 00 01 02 00 00 00", "ALT", "0", "2.4", "25", "10000", "50"],
        [u"ALT, 向下，1 ms/step，50 step，10000 ms，50 次", "05 32 27 10 32 05 00 01 02 00 00 00", "ALT", "0", "1", "50", "10000", "50"],
        [u"ALT, 向下，1 ms/step，25 step，8000 ms，50 次", "05 19 1F 40 32 05 00 01 02 00 00 00", "ALT", "0", "1", "25", "8000", "50"],
        [u"ALT, 向下，1 ms/step，25 step，10000 ms，50 次", "05 19 27 10 64 05 00 01 02 00 00 00", "ALT", "0", "1", "25", "10000", "100"],
        ]


for command in commands:
    print command[0]
    print command[1]
    if parameter_converter.convert(command[2:]) != False:
        print " ".join(parameter_converter.convert(command[2:])) + " (" + " ".join(command[2:]) + ")"
    print ""

# 命令错误检查测试

error_check_commands = [
        ["Empty command"],

        ["Unknown command", "ddd"],

        ["Parameter number wrong", "VD"],
        ["Parameter number wrong", "VD", "1"],
        ["Parameter number wrong", "VD", "1", "2", "3", "4"],
        ["Direction wrong", "VD", "-1", "2", "3"],
        ["Direction wrong", "VD", "2", "2", "3"],
        ["Direction wrong", "VD", "1.3", "2", "3"],
        ["Direction wrong", "VD", "a", "2", "3"],
        ["Interval wrong", "VD", "1", "a", "3"],
        ["Interval wrong", "VD", "1", "1.02", "3"],
        ["Interval wrong", "VD", "1", "0.0", "3"],
        ["Interval wrong", "VD", "1", "3.2", "3"],
        ["Interval wrong", "VD", "1", "2.1", "3"],
        ["Interval wrong", "VD", "1", "0", "3"],
        ["Interval wrong", "VD", "1", "65537", "3"],
        ["Count wrong", "VD", "1", "2", "a"],
        ["Count wrong", "VD", "1", "2", "1.0"],
        ["Count wrong", "VD", "1", "2", "-1"],
        ["Count wrong", "VD", "1", "2", "65536"],
        ["Count wrong", "VD", "1", "5", "65536"],
        ["Count wrong", "VD", "1", "5", "-1"],
        ["Count wrong", "VD", "1", "5", "256"],


        ["Parameter number wrong", "DELAY"],
        ["Parameter number wrong", "DELAY", "1", "2"],
        ["Interval wrong", "DELAY", "a"],
        ["Interval wrong", "DELAY", "1.0"],
        ["Interval wrong", "DELAY", "-1"],
        ["Interval wrong", "DELAY", "16711426"],

        ["Parameter number wrong", "ALT"],
        ["Parameter number wrong", "ALT", "1"],
        ["Parameter number wrong", "ALT", "1", "2", "3", "4", "5", "6"],
        ["Direction wrong", "ALT", "-1", "2", "3", "4", "5"],
        ["Direction wrong", "ALT", "2", "2", "3", "4", "5"],
        ["Direction wrong", "ALT", "1.3", "2", "3", "4", "5"],
        ["Direction wrong", "ALT", "a", "2", "3", "4", "5"],
        ["Step_interval wrong", "ALT", "1", "a", "3", "4", "5"],
        ["Step_interval wrong", "ALT", "1", "1.02", "3", "4", "5"],
        ["Step_interval wrong", "ALT", "1", "0.0", "3", "4", "5"],
        ["Step_interval wrong", "ALT", "1", "3.2", "3", "4", "5"],
        ["Step_interval wrong", "ALT", "1", "2.1", "3", "4", "5"],
        ["Step_interval wrong", "ALT", "1", "0", "3", "4", "5"],
        ["Step_interval wrong", "ALT", "1", "4", "3", "4", "5"],
        ["Step_count wrong", "ALT", "1", "2", "a", "4", "5"],
        ["Step_count wrong", "ALT", "1", "2", "1.0", "4", "5"],
        ["Step_count wrong", "ALT", "1", "2", "-2", "4", "5"],
        ["Step_count wrong", "ALT", "1", "2", "256", "4", "5"],
        ["Part_interval wrong", "ALT", "1", "2", "3", "a", "5"],
        ["Part_interval wrong", "ALT", "1", "2", "3", "1.0", "5"],
        ["Part_interval wrong", "ALT", "1", "2", "3", "-2", "5"],
        ["Part_interval wrong", "ALT", "1", "2", "3", "65536", "5"],
        ["Part_count wrong", "ALT", "1", "2", "3", "4", "a"],
        ["Part_count wrong", "ALT", "1", "2", "3", "4", "1.0"],
        ["Part_count wrong", "ALT", "1", "2", "3", "4", "-2"],
        ["Part_count wrong", "ALT", "1", "2", "3", "4", "256"],
        ]


for command in error_check_commands:
    print command[0] + " (" + " ".join(command[1:]) + ")"
    if parameter_converter.convert(command[1:]) != False:
        print parameter_converter.convert(command[1:])
    print ""
