#!/usr/bin/env python
# coding=utf-8

'''
These command take step length independent, decimal parameters that are directly
corresponding to the original code unit.
'''

from decimal import Decimal

class smcsc_command_direct:
    BACK_DIRECTION = "0"
    BACK_INTERVAL = "5"
    BACK_STEP_COUNT = "00"
    BACK_PAUSE_TIME_HIGH = "01"
    BACK_PAUSE_TIME_LOW = "02"

    END = ["00", "00", "00",]

    def convert(self, command):
        if command[0] == "VDH":
            '''
            direction       int     1   1, 0
            step_interval   float   ms  0.2--3.0, 0.2 * N
            step_count      int     1   0--255
            part_count      int     1   0--255
            '''
            direction = int(command[1])
            step_interval = Decimal(command[2])
            step_count = int(command[3])
            part_count = int(command[4])

            if direction == 1:
                a11 = "F"
            else:
                a11 = "0"

            a12 = "%1X" % (int(step_interval / Decimal("0.2")))
            a1 = a11 + a12
            a2 = "%02X" % (step_count)
            a3 = "00"
            a4 = "00"
            a5 = "%02X" % (part_count)

            a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
            a7 = self.BACK_STEP_COUNT
            a8 = self.BACK_PAUSE_TIME_HIGH
            a9 = self.BACK_PAUSE_TIME_LOW

            code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

        elif command[0] == "VDL":
            '''
            direction       int     1   1, 0
            part_interval   int     ms  3--65535
            part_count      int     1   0--255
            '''
            direction = int(command[1])
            part_interval = int(command[2])
            part_count = int(command[3])

            if direction == 1:
                a11 = "F"
            else:
                a11 = "0"

            a12 = "5"
            a1 = a11 + a12
            a2 = "01"
            a3 = "%02X" % (part_interval / 256)
            a4 = "%02X" % (part_interval % 256)
            a5 = "%02X" % (part_count)

            a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
            a7 = self.BACK_STEP_COUNT
            a8 = self.BACK_PAUSE_TIME_HIGH
            a9 = self.BACK_PAUSE_TIME_LOW

            code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

        elif command[0] == "DELAY":
            '''
            part_interval   int     ms  0--65535
            part_count      int     1   0--255
            '''
            part_interval = int(command[1])
            part_count = int(command[2])

            a1 = "05"
            a2 = "00"
            a3 = "%02X" % (part_interval / 256)
            a4 = "%02X" % (part_interval % 256)
            a5 = "%02X" % (part_count)

            a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
            a7 = self.BACK_STEP_COUNT
            a8 = self.BACK_PAUSE_TIME_HIGH
            a9 = self.BACK_PAUSE_TIME_LOW

            code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

        elif command[0] == "ALT":
            '''
            direction       int     1   1, 0
            step_interval   float   ms  0.2--3.0, 0.2 * N
            step_count      int     1   0--255
            part_interval   int     ms  0--65535
            part_count      int     1   0-255
            '''
            direction = int(command[1])
            step_interval = Decimal(command[2])
            step_count = int(command[3])
            part_interval = int(command[4])
            part_count = int(command[5])

            if direction == 1:
                a11 = "F"
            else:
                a11 = "0"

            a12 = "%1X" % (int(step_interval / Decimal("0.2")))
            a1 = a11 + a12
            a2 = "%02X" % (step_count)
            a3 = "%02X" % (part_interval / 256)
            a4 = "%02X" % (part_interval % 256)
            a5 = "%02X" % (part_count)

            a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
            a7 = self.BACK_STEP_COUNT
            a8 = self.BACK_PAUSE_TIME_HIGH
            a9 = self.BACK_PAUSE_TIME_LOW

            code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

        else:
            pass

        #return ''.join(code)
        return code