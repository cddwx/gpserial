#!/usr/bin/env python
# coding=utf-8

import sys
from smcsc_command_direct import smcsc_command_direct

parameter_converter = smcsc_command_direct()

# 测试代码
'''
# command direct

## VDH

direction       int     1   1, 0
step_interval   float   ms  0.2--3.0, 0.2 * N
step_count      int     1   0--255
part_count      int     1   0--255

向下，1 ms/step，125 step
向上，1 ms/step，125 step
向下，2.6 ms/step，125 step
向下，1 ms/step，510 step
'''

commands = [
        [u"VDH, 向下，1 ms/step，125 step", "05 7D 00 00 01 05 00 01 02 00 00 00", "VDH", "0", "1", "125", "1"],
        [u"VDH, 向上，1 ms/step，125 step", "F5 7D 00 00 01 05 00 01 02 00 00 00", "VDH", "1", "1", "125", "1"],
        [u"VDH, 向下，2.6 ms/step，125 step", "0D 7D 00 00 01 05 00 01 02 00 00 00", "VDH", "0", "2.6", "125", "1"],
        [u"VDH, 向下，1 ms/step，510 step", "05 FF 00 00 02 05 00 01 02 00 00 00", "VDH", "0", "1", "255", "2"],
        ]

'''
step_intervals = []
for i in range(1, 16):
    step_intervals.append(str(i * Decimal("0.2")))

for direction in ["1", "0"]:
    for step_interval in step_intervals:
        for step_count in range(0, 256):
            for part_count in range(0, 256):
                command = ["VDH", direction, step_interval, str(step_count), str(part_count)]
'''

'''
## VDL

direction       int     1   1, 0
part_interval   int     ms  3--65535
part_count      int     1   0--255

向下，4 ms/step，125 step
向上，4 ms/step，125 step
向下，65500 ms/step，125 step
'''
commands = commands + [
        [u"VDL, 向下，4 ms/step，125 step", "05 01 00 03 7D 05 00 01 02 00 00 00", "VDL", "0", "3", "125"],
        [u"VDL, 向上，4 ms/step，125 step", "05 01 00 03 7D 05 00 01 02 00 00 00", "VDL", "0", "3", "125"],
        [u"VDL, 向下，65500 ms/step，125 step", "05 01 FF DB 7D 05 00 01 02 00 00 00", "VDL", "0", "65499", "125"],
        ]

'''
## DELAY

part_interval   int     ms  0--65535
part_count      int     1   0--255

65530 ms
131070 ms
'''
commands = commands + [
        [u"DELAY, 65530 ms", "05 00 FF FA 01 05 00 01 02 00 00 00", "DELAY", "65530", "1"],
        [u"DELAY, 131070 ms", "05 00 FF FF 02 05 00 01 02 00 00 00", "DELAY", "65535", "2"],
        ]

'''
## ALT

direction       int     1   1, 0
step_interval   float   ms  0.2--3.0, 0.2 * N
step_count      int     1   0--255
part_interval   int     ms  0--65535
part_count      int     1   0-255


向下，1 ms/step，25 step，10000 ms，50 次
向上，1 ms/step，25 step，10000 ms，50 次
向下，2.4 ms/step，25 step，10000 ms，50 次
向下，1 ms/step，50 step，10000 ms，50 次
向下，1 ms/step，25 step，8000 ms，50 次
向下，1 ms/step，25 step，8000 ms，100 次
'''
commands = commands + [
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
    print " ".join(parameter_converter.convert(command[2:])) + " (" + " ".join(command[2:]) + ")"
    print ""