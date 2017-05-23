#!/usr/bin/env python
# coding=utf-8

import sys
from smcsc_command_natural import smcsc_command_natural

parameter_converter = smcsc_command_natural()

# 测试代码
'''
## VD

direction       int     1       1, 0
speed           float   um/s    f(step / 3.0)--f(step / 0.2) OR f(step / 65536)--f(step / 4)
distance        int     um      0--f(step * 65535) OR 0--f(step * 255)
step            float   um

1.557 um/step，向下，1000 um/s(1.6 ms/step)，800 um(514 step)
2.4 um/step，向下，1500 um/s(1.6 ms/step)，800 um(333 step)
1.557 um/step，向上，1000 um/s(1.6 ms/step)，800 um(514 step)
1.557 um/step，向下，649 um/s(2.4 ms/step)，800 um(514 step)
1.557 um/step，向下，1000 um/s(1.6 ms/step)，195 um(125 step)
1.557 um/step，向下，389 um/s(4 ms/step)，195 um(125 step)
1.557 um/step，向下，0.22243 um/s(7000 ms/step)，195 um(125 step)
'''

commands = [
        [u"1.557 um/step, 向下，1000 um/s(1.6 ms/step)，800 um(514 step)", "08 FF 00 00 02 05 00 01 02 08 04 00 00 01 05 00 01 02 00 00 00", "VD", "0", "1000", "800", "1.557"],
        [u"2.4 um/step, 向下，1500 um/s(1.6 ms/step)，800 um(333 step)", "08 FF 00 00 01 05 00 01 02 08 4E 00 00 01 05 00 01 02 00 00 00", "VD", "0", "1500", "800", "2.4"],
        [u"1.557 um/step, 向上，1000 um/s(1.6 ms/step)，800 um(514 step)", "F8 FF 00 00 02 05 00 01 02 F8 04 00 00 01 05 00 01 02 00 00 00", "VD", "1", "1000", "800", "1.557"],
        [u"1.557 um/step, 向下，649 um/s(2.4 ms/step)，800 um(514 step)", "0C FF 00 00 02 05 00 01 02 0C 04 00 00 01 05 00 01 02 00 00 00", "VD", "0", "649", "800", "1.557"],
        [u"1.557 um/step, 向下，1000 um/s(1.6 ms/step)，195 um(125 step)", "08 7D 00 00 01 05 00 01 02 00 00 00", "VD", "0", "1000", "195", "1.557"],
        [u"1.557 um/step, 向下，389 um/s(4 ms/step)，195 um(125 step)", "05 01 00 03 7D 05 00 01 02 00 00 00", "VD", "0", "389", "195", "1.557"],
        [u"1.557 um/step, 向下，0.00022243 um/s(7000 ms/step)，195 um(125 step)", "05 01 1B 57 7D 05 00 01 02 00 00 00", "VD", "0", "0.22243", "195", "1.557"],
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
## DELAY

interval    int     ms  0--65535 * 255

65530 ms
131070 ms
100000 ms
'''
commands = commands + [
        [u"DELAY, 65530 ms", "05 00 FF FA 01 05 00 01 02 00 00 00", "DELAY", "65530"],
        [u"DELAY, 131070 ms", "05 00 FF FF 02 05 00 01 02 00 00 00", "DELAY", "131070"],
        [u"DELAY, 100000 ms", "05 00 FF FF 01 05 00 01 02 05 00 86 A1 01 05 00 01 02 00 00 00", "DELAY", "100000"],
        ]

'''
## ALT

direction       int     1       1, 0
speed           float   um/s    f(step / 3.0)--f(step / 0.2)
distance        int     um      0--f(step * 65535)
interval        int     ms      0--65535
count           int     1       0--255
step            float   um


1.557 um/step，向下，1557 um/s(1 ms/step)，39 um(25 step)，10000 ms，50 次
2.4 um/step，向下，2400 um/s(1 ms/step)，60 um(25 step)，10000 ms，50 次
1.557 um/step，向上，1557 um/s(1 ms/step)，38 um(25 step)，10000 ms，50 次
1.557 um/step，向下，649 um/s(2.4 ms/step)，39 um(25 step)，10000 ms，50 次
1.557 um/step，向下，1557 um/s(1 ms/step)，78 um(50 step)，10000 ms，50 次
1.557 um/step，向下，1557 um/s(1 ms/step)，39 um(25 step)，8000 ms，50 次
1.557 um/step，向下，1557 um/s(1 ms/step)，39 um(25 step)，10000 ms，100 次
'''
commands = commands + [
        [u"ALT, 1.557 um/step，向下，1557 um/s(1 ms/step)，39 um(25 step)，10000 ms，50 次", "05 19 27 10 32 05 00 01 02 00 00 00", "ALT", "0", "1557", "39", "10000", "50", "1.557"],
        [u"ALT, 2.4 um/step，向下，2400 um/s(1 ms/step)，60 um(25 step)，10000 ms，50 次", "05 19 27 10 32 05 00 01 02 00 00 00", "ALT", "0", "2400", "60", "10000", "50", "2.4"],
        [u"ALT, 1.557 um/step，向上，1557 um/s(1 ms/step)，39 um(25 step)，10000 ms，50 次", "F5 19 27 10 32 05 00 01 02 00 00 00", "ALT", "1", "1557", "39", "10000", "50", "1.557"],
        [u"ALT, 1.557 um/step，向下，649 um/s(2.4 ms/step)，39 um(25 step)，10000 ms，50 次", "0C 19 27 10 32 05 00 01 02 00 00 00", "ALT", "0", "1557", "39", "10000", "50", "1.557"],
        [u"ALT, 1.557 um/step，向下，1557 um/s(1 ms/step)，78 um(50 step)，10000 ms，50 次", "05 32 27 10 32 05 00 01 02 00 00 00", "ALT", "0", "1557", "78", "10000", "50", "1.557"],
        [u"ALT, 1.557 um/step，向下，1557 um/s(1 ms/step)，39 um(25 step)，8000 ms，50 次", "05 19 1F 40 32 05 00 01 02 00 00 00", "ALT", "0", "1557", "39", "8000", "50", "1.557"],
        [u"ALT, 1.557 um/step，向下，1557 um/s(1 ms/step)，39 um(25 step)，10000 ms，100 次", "05 19 27 10 64 05 00 01 02 00 00 00", "ALT", "0", "1557", "39", "10000", "100", "1.557"],
        ]


for command in commands:
    print command[0]
    print command[1]
    print " ".join(parameter_converter.convert(command[2:])) + " (" + " ".join(command[2:]) + ")"
    print ""