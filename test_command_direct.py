#!/usr/bin/env python
# coding=utf-8

import sys
from smcsc_command_direct import smcsc_command_direct

parameter_converter = smcsc_command_direct()

# 代码生成测试

commands = [
        [u"VDH, 向下，1 ms/step，125 step", "05 7D 00 00 01 05 00 01 02 00 00 00", "VDH", "0", "1", "125", "1"],
        [u"VDH, 向上，1 ms/step，125 step", "F5 7D 00 00 01 05 00 01 02 00 00 00", "VDH", "1", "1", "125", "1"],
        [u"VDH, 向下，2.6 ms/step，125 step", "0D 7D 00 00 01 05 00 01 02 00 00 00", "VDH", "0", "2.6", "125", "1"],
        [u"VDH, 向下，1 ms/step，510 step", "05 FF 00 00 02 05 00 01 02 00 00 00", "VDH", "0", "1", "255", "2"],

        [u"VDL, 向下，4 ms/step，125 step", "05 01 00 03 7D 05 00 01 02 00 00 00", "VDL", "0", "3", "125"],
        [u"VDL, 向上，4 ms/step，125 step", "05 01 00 03 7D 05 00 01 02 00 00 00", "VDL", "0", "3", "125"],
        [u"VDL, 向下，65500 ms/step，125 step", "05 01 FF DB 7D 05 00 01 02 00 00 00", "VDL", "0", "65499", "125"],

        [u"DELAY, 65530 ms", "05 00 FF FA 01 05 00 01 02 00 00 00", "DELAY", "65530", "1"],
        [u"DELAY, 131070 ms", "05 00 FF FF 02 05 00 01 02 00 00 00", "DELAY", "65535", "2"],

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
    try:
        print " ".join(parameter_converter.convert(command[2:])) + " (" + " ".join(command[2:]) + ")"

    except Exception as e:
        print "[Error   ] ", e

    else:
        pass

    print ""

# 命令错误检查测试

error_check_commands = [
        ["Empty command"],

        ["Unknown command", "ddd"],

        ["Parameter number wrong", "VDH"],
        ["Parameter number wrong", "VDH", "1"],
        ["Parameter number wrong", "VDH", "1", "2", "3", "4", "3"],
        ["Direction wrong", "VDH", "-1", "2", "3", "4"],
        ["Direction wrong", "VDH", "2", "2", "3", "4"],
        ["Direction wrong", "VDH", "1.3", "2", "3", "4"],
        ["Direction wrong", "VDH", "a", "2", "3", "4"],
        ["Step_interval wrong", "VDH", "1", "a", "3", "4"],
        ["Step_interval wrong", "VDH", "1", "1.02", "3", "4"],
        ["Step_interval wrong", "VDH", "1", "0.0", "3", "4"],
        ["Step_interval wrong", "VDH", "1", "3.2", "3", "4"],
        ["Step_interval wrong", "VDH", "1", "2.1", "3", "4"],
        ["Step_interval wrong", "VDH", "1", "0", "3", "4"],
        ["Step_interval wrong", "VDH", "1", "4", "3", "4"],
        ["Step_count wrong", "VDH", "1", "2", "a", "4"],
        ["Step_count wrong", "VDH", "1", "2", "1.0", "4"],
        ["Step_count wrong", "VDH", "1", "2", "-2", "4"],
        ["Step_count wrong", "VDH", "1", "2", "256", "4"],
        ["Part_count wrong", "VDH", "1", "2", "3", "a"],
        ["Part_count wrong", "VDH", "1", "2", "3", "1.0"],
        ["Part_count wrong", "VDH", "1", "2", "3", "-2"],
        ["Part_count wrong", "VDH", "1", "2", "3", "256"],

        ["Parameter number wrong", "VDL"],
        ["Parameter number wrong", "VDL", "1"],
        ["Parameter number wrong", "VDL", "1", "5", "3", "4"],
        ["Direction wrong", "VDL", "-1", "5", "3"],
        ["Direction wrong", "VDL", "2", "5", "3"],
        ["Direction wrong", "VDL", "1.3", "5", "3"],
        ["Direction wrong", "VDL", "a", "5", "3"],
        ["Part_interval wrong", "VDL", "1", "a", "3"],
        ["Part_interval wrong", "VDL", "1", "1.0", "3"],
        ["Part_interval wrong", "VDL", "1", "-2", "3"],
        ["Part_interval wrong", "VDL", "1", "65536", "3"],
        ["Part_count wrong", "VDL", "1", "3", "a"],
        ["Part_count wrong", "VDL", "1", "3", "1.0"],
        ["Part_count wrong", "VDL", "1", "3", "-2"],
        ["Part_count wrong", "VDL", "1", "3", "256"],

        ["Parameter number wrong", "DELAY"],
        ["Parameter number wrong", "DELAY", "1"],
        ["Parameter number wrong", "DELAY", "1", "2", "3"],
        ["Part_interval wrong", "DELAY", "1", "a", "3"],
        ["Part_interval wrong", "DELAY", "1", "1.0", "3"],
        ["Part_interval wrong", "DELAY", "1", "-2", "3"],
        ["Part_interval wrong", "DELAY", "1", "65536", "3"],
        ["Part_count wrong", "DELAY", "1", "3", "a"],
        ["Part_count wrong", "DELAY", "1", "3", "1.0"],
        ["Part_count wrong", "DELAY", "1", "3", "-2"],
        ["Part_count wrong", "DELAY", "1", "3", "256"],

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
    try:
        print parameter_converter.convert(command[1:])

    except Exception as e:
        print "[Error   ] ", e

    else:
        pass

    print ""
