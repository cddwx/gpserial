#!/usr/bin/env python
# coding=utf-8

import os
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
        self.event_run_finished = threading.Event()

    def run(self):
        while (not self.event_stop.is_set()):
            try:
                '''
                This line always cause a IOErroro when I close serial port, so I catch it and exit thread.
                Traceback (most recent call last):
                  File "/usr/lib/python2.7/threading.py", line 801, in __bootstrap_inner
                      self.run()
                  File "/home/fjc/documents/1-lab/5-实验工具/5-机械装置/浸涂机-OY/控制程序/步进电机分段控制-1.4/client/smcsc/core/serial_read_thread.py", line 24, in run
                      (self.main_window.serial_port.inWaiting())
                  File "/usr/local/lib/python2.7/dist-packages/serial/serialutil.py", line 529, in inWaiting
                      return self.in_waiting
                  File "/usr/local/lib/python2.7/dist-packages/serial/serialposix.py", line 464, in in_waiting
                      s = fcntl.ioctl(self.fd, TIOCINQ, TIOCM_zero_str)
                  IOError: [Errno 9] Bad file descriptor
                '''
                in_waiting = self.main_window.serial_port.inWaiting()
            except (ValueError, Exception) as e:
                return

            if (in_waiting > 0):
                try:
                    text = self.main_window.serial_port.read(in_waiting)
                except (ValueError, Exception) as e:
                    wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)

                else:
                    wx.CallAfter(pub.sendMessage, "update", data = text)

                try:
                    run_seq = self.main_window.run_thread.event_run_seq.is_set()
                except (ValueError, Exception) as e:
                    pass
                else:
                    if (
                            (run_seq) and
                            (text == "Running finished.\x0D\x0A\x0D\x0A")
                    ):
                        self.event_run_finished.set()

                    else:
                        pass

            else:
                pass

            # This is necessary, or it cost huge CPU
            time.sleep(0.01)
