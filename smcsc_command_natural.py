#!/usr/bin/env python
# coding=utf-8

'''
These command take step length dependent, decimal, pratical meaning parameters that are not
directly coresponding to the original code unit.

Command format:

VD {step} {direction} {speed} {distance}
DELAY {interval}
ALT {step} {direction} {speed} {distance} {interval} {count}
'''

from decimal import Decimal, ROUND_HALF_UP, ROUND_UP, ROUND_DOWN

class smcsc_command_natural:
    BACK_DIRECTION = "0"
    BACK_INTERVAL = "5"
    BACK_STEP_COUNT = "00"
    BACK_PAUSE_TIME_HIGH = "01"
    BACK_PAUSE_TIME_LOW = "02"

    END = ["00", "00", "00",]

    def convert(self, command):
        if command == []:
            error = '''Command is empty.
    Availiable commands:
    VD {step} {direction} {speed} {distance}
    DELAY {interval}
    ALT {step} {direction} {speed} {distance} {interval} {count}'''
            raise Exception(error)

        if command[0] == "VD":
            '''
            step            float   um
            direction       int     1       1, 0
            speed           float   um/s    f(step / 65536 * 1000)--f(step / 4 * 1000) OR f(step / 3.0 * 1000)--f(step / 0.2 * 1000)
            distance        int     um      0--f(step * 255) OR 0--f(step * 65535)
            '''

            if len(command[1:]) != 4:
                error_tmp = '''In "%s", the number of parameter is wrong
    Parameters:
    step            float   um
    direction       int     1       1, 0
    speed           float   um/s    f(step / 65536 * 1000)--f(step / 4 * 1000) OR f(step / 3.0 * 1000)--f(step / 0.2 * 1000)
    distance        int     um      0--f(step * 255) OR 0--f(step * 65535)'''
                error = error_tmp % (" ".join(command))
                raise Exception(error)

            if ((not self.is_int(command[1])) and (not self.is_float(command[1]))):
                error_tmp = '''In "%s", the step "%s" is wrong.'''
                error = error_tmp % (" ".join(command), command[1])
                raise Exception(error)

            if command[2] not in ["1", "0"]:
                error_tmp = '''In "%s", the direction "%s" is wrong.'''
                error = error_tmp % (" ".join(command), command[2])
                raise Exception(error)

            slow_begin = (Decimal(command[1]) / 65536 * 1000).quantize(Decimal("0.001"), rounding=ROUND_UP)
            slow_end = (Decimal(command[1]) / 4 * 1000).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
            fast_begin = (Decimal(command[1]) / 3 * 1000).quantize(Decimal("0.001"), rounding=ROUND_UP)
            fast_end = (Decimal(command[1]) / Decimal("0.2") * 1000).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
            if ((not self.is_int(command[3])) and (not self.is_float(command[3]))) or ((Decimal(command[3]) < slow_begin) or ((Decimal(command[3]) > slow_end) and (Decimal(command[3]) < fast_begin)) or (Decimal(command[3]) > fast_end)):
                error_tmp = '''In "%s", the speed "%s" is wrong
    The range for current step "%s" is %s -- %s and %s -- %s.'''
                error = error_tmp  % (" ".join(command), command[3], command[1], slow_begin, slow_end, fast_begin, fast_end)
                raise Exception(error)

            little_end = (Decimal(command[1]) * 255).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
            more_end = (Decimal(command[1]) * 65535).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
            if (not self.is_int(command[4])) or (((Decimal(command[3]) <= slow_end) and ((int(command[4]) < 0) or (int(command[4]) > little_end))) or ((Decimal(command[3]) >= fast_begin) and ((int(command[4]) < 0) or (int(command[4]) > more_end)))):
                error_tmp = '''In "%s", the distance "%s" is wrong
    The range for current step "%s" is %s -- %s when speed at %s -- %s and %s -- %s when speed at %s -- %s.'''
                error = error_tmp  % (" ".join(command), command[4], command[1], 0, little_end, slow_begin, slow_end, 0, more_end, fast_begin, fast_end)
                raise Exception(error)

            step = Decimal(command[1])
            direction = int(command[2])
            speed = Decimal(command[3])
            distance = int(command[4])

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
                    return code

                elif count % 255 == 0:
                    a2 = "FF"
                    a5 = "%02X" % (count / 255)

                    a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
                    a7 = self.BACK_STEP_COUNT
                    a8 = self.BACK_PAUSE_TIME_HIGH
                    a9 = self.BACK_PAUSE_TIME_LOW

                    code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END
                    return code

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
                    return code

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
                return code

            else:
                pass

        elif command[0] == "DELAY":
            '''
            interval    int     ms  0--65535 * 255
            '''

            if len(command[1:]) != 1:
                error_tmp = '''In "%s", the number of parameter is wrong
    Parameters:
    interval    int     ms  0--65535 * 255'''
                error = error_tmp % (" ".join(command))
                raise Exception(error)

            if (not self.is_int(command[1])) or ((int(command[1]) < 0) or (int(command[1]) > (65535 * 255))):
                error_tmp = '''In "%s", the interval "%s" is wrong.'''
                error = error_tmp % (" ".join(command), command[1])
                raise Exception(error)

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
                return code

            elif interval % 65535 == 0:
                a3 = "FF"
                a4 = "FF"
                a5 = "%02X" % (interval / 65535)

                a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
                a7 = self.BACK_STEP_COUNT
                a8 = self.BACK_PAUSE_TIME_HIGH
                a9 = self.BACK_PAUSE_TIME_LOW

                code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END
                return code

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
                return code

            else:
                pass

        elif command[0] == "ALT":
            '''
            step            float   um
            direction       int     1       1, 0
            speed           float   um/s    f(step / 3.0 * 1000)--f(step / 0.2 * 1000)
            distance        int     um      0--f(step * 255)
            interval        int     ms      0--65535
            count           int     1       0--255
            '''

            if len(command[1:]) != 6:
                error_tmp = '''In "%s", the number of parameter is wrong
    Parameters:
    step            float   um
    direction       int     1       1, 0
    speed           float   um/s    f(step / 3.0 * 1000)--f(step / 0.2 * 1000)
    distance        int     um      0--f(step * 255)
    interval        int     ms      0--65535
    count           int     1       0--255'''
                error = error_tmp % (" ".join(command))
                raise Exception(error)

            if ((not self.is_int(command[1])) and (not self.is_float(command[1]))):
                error_tmp = '''In "%s", the step "%s" is wrong.'''
                error = error_tmp % (" ".join(command), command[1])
                raise Exception(error)

            if command[2] not in ["1", "0"]:
                error_tmp = '''In "%s", the direction "%s" is wrong.'''
                error = error_tmp % (" ".join(command), command[2])
                raise Exception(error)

            fast_begin = (Decimal(command[1]) / 3 * 1000).quantize(Decimal("0.001"), rounding=ROUND_UP)
            fast_end = (Decimal(command[1]) / Decimal("0.2") * 1000).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
            if ((not self.is_int(command[3])) and (not self.is_float(command[3]))) or ((Decimal(command[3]) < fast_begin) or (Decimal(command[3]) > fast_end)):
                error_tmp = '''In "%s", the speed "%s" is wrong
    The range for current step "%s" is %s -- %s.'''
                error = error_tmp % (" ".join(command), command[3], command[1], fast_begin, fast_end)
                raise Exception(error)

            little_end = (Decimal(command[1]) * 255).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
            if (not self.is_int(command[4])) or ((int(command[4]) < 0) or (int(command[4]) > little_end)):
                error_tmp = '''In "%s", the distance "%s" is wrong
    The range for current step "%s" is %s -- %s.'''
                error = error_tmp % (" ".join(command), command[4], command[1], 0, little_end)
                raise Exception(error)

            if (not self.is_int(command[5])) or (int(command[5]) < 0 or int(command[5]) > 65535):
                error_tmp = '''In "%s", the interval "%s" is wrong.'''
                error = error_tmp % (" ".join(command), command[5])
                raise Exception(error)

            if (not self.is_int(command[6])) or (int(command[6]) < 0 or int(command[6]) > 255):
                error_tmp = '''In "%s", the count "%s" is wrong.'''
                error = error_tmp % (" ".join(command), command[6])
                raise Exception(error)

            step = Decimal(command[1])
            direction = int(command[2])
            speed = Decimal(command[3])
            distance = int(command[4])
            interval = int(command[5])
            count = int(command[6])

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
            return code

        else:
            error = '''Unknown command.'''
            raise Exception(error)

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
