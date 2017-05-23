#!/usr/bin/env python
# coding=utf-8

'''
These command take step length dependent, decimal, pratical meaning parameters that are not
directly coresponding to the original code unit.
'''

from decimal import Decimal, ROUND_HALF_UP

class smcsc_command_natural:
    BACK_DIRECTION = "0"
    BACK_INTERVAL = "5"
    BACK_STEP_COUNT = "00"
    BACK_PAUSE_TIME_HIGH = "01"
    BACK_PAUSE_TIME_LOW = "02"

    END = ["00", "00", "00",]

    def convert(self, command):
        if command[0] == "VD":
            '''
            direction       int     1       1, 0
            speed           float   um/s    f(step / 3.0)--f(step / 0.2) OR f(step / 65536)--f(step / 4)
            distance        int     um      0--f(step * 65535) OR 0--f(step * 255)
            step            float   um
            '''
            direction = int(command[1])
            speed = Decimal(command[2])
            distance = int(command[3])
            step = Decimal(command[4])

            if direction == 1:
                a11 = "F"
            else:
                a11 = "0"

            interval = (step / speed * 1000).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            if interval <= Decimal("3.00"):
                if ((int(interval * 100) / 10) % 2) == 0:
                    interval_real = Decimal(str(int(interval * 100) / 10)) / Decimal("10")

                elif ((int(interval * 100) / 10) % 2) != 0:
                    interval_real = Decimal(str((int(interval * 100) / 10) + 1)) / Decimal("10")

                else:
                    pass

                count = int((distance / step).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

                a12 = "%1X" % (interval_real / Decimal("0.2"))
                a1 = a11 + a12
                a3 = "00"
                a4 = "00"

                if count <= 255:
                    a2 = "%02X" % (count)
                    a5 = "01"

                    a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
                    a7 = self.BACK_STEP_COUNT
                    a8 = self.BACK_PAUSE_TIME_HIGH
                    a9 = self.BACK_PAUSE_TIME_LOW

                    code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

                elif count % 255 == 0:
                    a2 = "FF"
                    a5 = "%02X" % (count / 255)

                    a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
                    a7 = self.BACK_STEP_COUNT
                    a8 = self.BACK_PAUSE_TIME_HIGH
                    a9 = self.BACK_PAUSE_TIME_LOW

                    code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

                elif count % 255 != 0:
                    a2 = "FF"
                    a5 = "%02X" % (count / 255)

                    a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
                    a7 = self.BACK_STEP_COUNT
                    a8 = self.BACK_PAUSE_TIME_HIGH
                    a9 = self.BACK_PAUSE_TIME_LOW

                    a1_2 = a1
                    a2_2 = "%02X" % (count % 255)
                    a3_2 = a3
                    a4_2 = a4
                    a5_2 = "01"

                    a6_2 = a6
                    a7_2 = a7
                    a8_2 = a8
                    a9_2 = a9

                    code = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a1_2, a2_2, a3_2, a4_2, a5_2, a6_2, a7_2, a8_2, a9_2,] + self.END

                else:
                    pass

            elif interval >= Decimal("4.00"):
                interval_real = interval.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
                count = int((distance / step).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
                a12 = "5"
                a1 = a11 + a12
                a2 = "01"
                a3 = "%02X" % ((int(interval_real) - 1) / 256)
                a4 = "%02X" % ((int(interval_real) - 1) % 256)
                a5 = "%02X" % (count)

                a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
                a7 = self.BACK_STEP_COUNT
                a8 = self.BACK_PAUSE_TIME_HIGH
                a9 = self.BACK_PAUSE_TIME_LOW

                code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

            else:
                pass

        elif command[0] == "DELAY":
            '''
            interval    int     ms  0--65535 * 255
            '''
            interval = int(command[1])

            a1 = "05"
            a2 = "00"

            if interval <= 65535:
                a3 = "%02X" % (interval / 256)
                a4 = "%02X" % (interval % 256)
                a5 = "01"

                a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
                a7 = self.BACK_STEP_COUNT
                a8 = self.BACK_PAUSE_TIME_HIGH
                a9 = self.BACK_PAUSE_TIME_LOW

                code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

            elif interval % 65535 == 0:
                a3 = "FF"
                a4 = "FF"
                a5 = "%02X" % (interval / 65535)

                a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
                a7 = self.BACK_STEP_COUNT
                a8 = self.BACK_PAUSE_TIME_HIGH
                a9 = self.BACK_PAUSE_TIME_LOW

                code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

            elif interval % 65535 != 0:
                a3 = "FF"
                a4 = "FF"
                a5 = "%02X" % (interval / 65535)

                a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
                a7 = self.BACK_STEP_COUNT
                a8 = self.BACK_PAUSE_TIME_HIGH
                a9 = self.BACK_PAUSE_TIME_LOW

                a1_2 = a1
                a2_2 = a2
                a3_2 = "%02X" % ((interval % 65535) / 256)
                a4_2 = "%02X" % ((interval % 65535) % 256)
                a5_2 = "01"

                a6_2 = a6
                a7_2 = a7
                a8_2 = a8
                a9_2 = a9

                code = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a1_2, a2_2, a3_2, a4_2, a5_2, a6_2, a7_2, a8_2, a9_2,] + self.END

            else:
                pass

        elif command[0] == "ALT":
            '''
            direction       int     1       1, 0
            speed           float   um/s
            distance        int     um
            interval        int     ms      0--65535
            count           int     1       0--255
            step            float   um
            '''
            direction = int(command[1])
            speed = Decimal(command[2])
            distance = int(command[3])
            interval = int(command[4])
            count = int(command[5])
            step = Decimal(command[6])

            if direction == 1:
                a11 = "F"
            else:
                a11 = "0"

            step_interval = (step / speed * 1000).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            if ((int(step_interval * 100) / 10) % 2) == 0:
                step_interval_real = Decimal(str(int(step_interval * 100) / 10)) / Decimal("10")
            elif ((int(step_interval * 100) / 10) % 2) != 0:
                step_interval_real = Decimal(str((int(step_interval * 100) + 1) / 10)) / Decimal("10")
            else:
                pass

            step_count = int((distance / step).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
            part_interval = interval
            part_count = count

            a12 = "%1X" % (int(step_interval_real / Decimal("0.2")))
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
