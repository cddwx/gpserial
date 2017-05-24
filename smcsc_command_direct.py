#!/usr/bin/env python
# coding=utf-8

'''
These command take step length independent, decimal parameters that are directly
corresponding to the original code unit.

Command format:

VDH {direction} {step_interval} {step_count} {part_count}
VDL {direction} {part_interval} {part_count}
DELAY {part_interval} {part_count}
ALT {direction} {step_interval} {step_count} {part_interval} {part_count}
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
        if command == []:
            print "[Error   ] Command is empty."
            print '''Availiable command:
VDH {direction} {step_interval} {step_count} {part_count}
VDL {direction} {part_interval} {part_count}
DELAY {part_interval} {part_count}
ALT {direction} {step_interval} {step_count} {part_interval} {part_count}'''
            return False

        elif command[0] == "VDH":
            '''
            direction       int     1   1, 0
            step_interval   float   ms  0.2--3.0, 0.2 * N
            step_count      int     1   0--255
            part_count      int     1   0--255
            '''
            if len(command[1:]) != 4:
                print "[Error   ] The number of parameter is wrong."
                print '''Parameters:
direction       int     1   1, 0
step_interval   float   ms  0.2--3.0, 0.2 * N
step_count      int     1   0--255
part_count      int     1   0--255'''
                return False

            if command[1] not in ["1", "0"]:
                print "[Error   ] The direction is wrong."
                return False

            if ((not self.is_int(command[2])) and (not self.is_float(command[2]))) or (self.is_float(command[2]) and (((len(command[2]) - (command[2].index(".") + 1)) > 1) or (Decimal(command[2]) < Decimal("0.2") or Decimal(command[2]) > Decimal("3.0")) or (int(Decimal(command[2]) * 10) % 2 != 0))) or (self.is_int(command[2]) and ((int(command[2]) < 1) or (int(command[2]) > 3))):
                print "[Error   ] The step_interval is wrong."
                return False

            if (not self.is_int(command[3])) or (int(command[3]) < 0 or int(command[3]) > 255):
                print "[Error   ] The step_count is wrong."
                return False

            if (not self.is_int(command[4])) or (int(command[4]) < 0 or int(command[4]) > 255):
                print "[Error   ] The part_count is wrong."
                return False

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
            return code

        elif command[0] == "VDL":
            '''
            direction       int     1   1, 0
            part_interval   int     ms  3--65535
            part_count      int     1   0--255
            '''
            if len(command[1:]) != 3:
                print "[Error   ] The number of parameter is wrong."
                print ''' Parameters:
direction       int     1   1, 0
part_interval   int     ms  3--65535
part_count      int     1   0--255'''
                return False

            if command[1] not in ["1", "0"]:
                print "[Error   ] The direction is wrong."
                return False

            if (not self.is_int(command[2])) or (int(command[2]) < 3 or int(command[2]) > 65535):
                print "[Error   ] The part_interval is wrong."
                return False

            if (not self.is_int(command[3])) or (int(command[3]) < 0 or int(command[3]) > 255):
                print "[Error   ] The part_count is wrong."
                return False

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
            return code

        elif command[0] == "DELAY":
            '''
            part_interval   int     ms  0--65535
            part_count      int     1   0--255
            '''

            if len(command[1:]) != 2:
                print "[Error   ] The number of parameter is wrong."
                print '''Parameters:
part_interval   int     ms  0--65535
part_count      int     1   0--255'''
                return False

            if (not self.is_int(command[1])) or (int(command[1]) < 0 or int(command[1]) > 65535):
                print "[Error   ] The part_interval is wrong."
                return False

            if (not self.is_int(command[2])) or (int(command[2]) < 0 or int(command[2]) > 255):
                print "[Error   ] The part_count is wrong."
                return False

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
            return code

        elif command[0] == "ALT":
            '''
            direction       int     1   1, 0
            step_interval   float   ms  0.2--3.0, 0.2 * N
            step_count      int     1   0--255
            part_interval   int     ms  0--65535
            part_count      int     1   0-255
            '''

            if len(command[1:]) != 5:
                print "[Error   ] The number of parameter is wrong."
                print '''
direction       int     1   1, 0
step_interval   float   ms  0.2--3.0, 0.2 * N
step_count      int     1   0--255
part_interval   int     ms  0--65535
part_count      int     1   0-255'''
                return False

            if command[1] not in ["1", "0"]:
                print "[Error   ] The direction is wrong."
                return False

            if ((not self.is_int(command[2])) and (not self.is_float(command[2]))) or (self.is_float(command[2]) and (((len(command[2]) - (command[2].index(".") + 1)) > 1) or (Decimal(command[2]) < Decimal("0.2") or Decimal(command[2]) > Decimal("3.0")) or (int(Decimal(command[2]) * 10) % 2 != 0))) or (self.is_int(command[2]) and ((int(command[2]) < 1) or (int(command[2]) > 3))):
                print "[Error   ] The step_interval is wrong."
                return False

            if (not self.is_int(command[3])) or (int(command[3]) < 0 or int(command[3]) > 255):
                print "[Error   ] The step_count is wrong."
                return False

            if (not self.is_int(command[4])) or (int(command[4]) < 0 or int(command[4]) > 65535):
                print "[Error   ] The part_interval is wrong."
                return False

            if (not self.is_int(command[5])) or (int(command[5]) < 0 or int(command[5]) > 255):
                print "[Error   ] The part_count is wrong."
                return False

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
            return code

        else:
            print "[Error   ] Unknown command."
            return False

    def is_int(self, string):
        try:
            int(string)
            return True

        except ValueError:
            return False

    def is_float(self, string):
        try:
            float(string)
            if not self.is_int(string):
                return True
            else:
                return False

        except ValueError:
            return False
