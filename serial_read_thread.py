#!/usr/bin/env python
# coding=utf-8

import time
import threading
import wx

from wx.lib.pubsub import pub

class serial_read_thread(threading.Thread):
    def __init__(self, serial_port, main_window):
        threading.Thread.__init__(self)

        self.serial_port = serial_port
        self.main_window = main_window

        self.event_stop = threading.Event()
        self.event_run_seq = threading.Event()
        self.event_run_finished = threading.Event()

    def run(self):
        while (not self.event_stop.is_set()):
            try:
                '''
                This line always cause a IOErroro when I close serial port, so I catch it and exit thread.
                Traceback (most recent call last):
                    ...
                  File "/usr/local/lib/python2.7/dist-packages/serial/serialposix.py", line 464, in in_waiting
                      s = fcntl.ioctl(self.fd, TIOCINQ, TIOCM_zero_str)
                  IOError: [Errno 9] Bad file descriptor
                '''
                in_waiting = self.serial_port.inWaiting()
            except (ValueError, Exception) as e:
                return


            if (self.event_run_seq.is_set() == True):
                #print in_waiting
                try:
                    text = self.serial_port.read(len("Running ...\x0D\x0A"))
                except (ValueError, Exception) as e:
                    wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)

                wx.CallAfter(pub.sendMessage, "update", data = text)


                count = 0
                text = ""
                while (
                        (count < len("Running finished.\x0D\x0A\x0D\x0A")) and
                        (self.event_run_seq.is_set() == True)
                ):
                    try:
                        in_waiting = self.serial_port.inWaiting()
                    except (ValueError, Exception) as e:
                        return

                    if (in_waiting > 0):
                        #print in_waiting
                        try:
                            text = text + self.serial_port.read(in_waiting)
                        except (ValueError, Exception) as e:
                            wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)

                        count = count + in_waiting
                    else:
                        pass

                    time.sleep(0.01)

                if (text == "Running finished.\x0D\x0A\x0D\x0A"):
                    wx.CallAfter(pub.sendMessage, "update", data = text)
                    self.event_run_finished.set()
                else:
                    pass
            else:
                if (in_waiting > 0):
                    try:
                        text = self.serial_port.read(in_waiting)
                    except (ValueError, Exception) as e:
                        wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)
                    else:
                        wx.CallAfter(pub.sendMessage, "update", data = text)
                else:
                    pass

            # This is necessary, or it cost huge CPU
            time.sleep(0.01)
