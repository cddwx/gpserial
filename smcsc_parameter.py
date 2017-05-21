#!/usr/bin/env python
# coding=utf-8

class smcsc_parameter:
    BACK_DIRECTION = "0"
    BACK_INTERVAL = "5"
    BACK_STEP_COUNT = "00"
    BACK_PAUSE_TIME_HIGH = "01"
    BACK_PAUSE_TIME_LOW = "02"

    END = ["00", "00", "00",]

    def move(self, parameter):
        direction       = int(parameter[0])
        step_interval   = float(parameter[1])
        step_count      = int(parameter[2])
        interval        = float(parameter[3])
        count           = int(parameter[4])

        # True point "F", move up direction.
        if direction == 1:
            a11 = "F"
        else:
            a11 = "0"

        a12 = "%1X" % (int(step_interval / 0.2))
        a1 = a11 + a12
        a2 = "%02X" % (step_count)
        a3 = "%02X" % (int((interval * 1000) / 256))
        a4 = "%02X" % (int((interval * 1000) % 256))
        a5 = "%02X" % (count)

        a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
        a7 = self.BACK_STEP_COUNT
        a8 = self.BACK_PAUSE_TIME_HIGH
        a9 = self.BACK_PAUSE_TIME_LOW

        list = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END

        #return ''.join(list)
        return list

    def command(self, command):
        if command[0] == "VDL":
            direction = command[1]
            interval = command[2]
            count = command[3]

            parameter = [direction, 1, 1, interval, count]
            code = self.move(parameter)

            return code

        elif command[0] == "VDH":
            direction = command[1]
            step_interval = command[2]
            step_count = command[3]
            count = command[4]

            parameter = [direction, step_interval, step_count, 0, count]
            code = self.move(parameter)

            return code

        elif command[0] == "DELAY":
            interval = command[1]
            count = command[2]

            parameter = [0, 1, 0, interval, count]
            code = self.move(parameter)

            return code

        elif command[0] == "ALT":
            direction = command[1]
            step_interval = command[2]
            step_count = command[3]
            interval = command[4]
            count = command[5]

            parameter = [direction, step_interval, step_count, step, count]
            code = self.move(parameter)

            return code

        else:
            pass
