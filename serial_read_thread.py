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
            if (self.event_run_seq.is_set() == True):
                count = 0
                text = ""
                while (
                        (count < len("Running ...\x0D\x0A")) and
                        (self.event_run_seq.is_set() == True)
                ):
                    try:
                        in_waiting = self.serial_port.inWaiting()
                    except (IOError) as e:
                        print "Serial_read_thread.run in_waiting: " + e.message
                        wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)
                        continue

                    if (in_waiting > 0):
                        if ((count + in_waiting) <= len("Running ...\x0D\x0A")):
                            #print in_waiting
                            try:
                                one_text = self.serial_port.read(in_waiting)
                            except (ValueError, Exception) as e:
                                wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)

                            text = text + one_text
                            count = count + in_waiting
                        else:
                            try:
                                one_text = self.serial_port.read(len("Running ...\x0D\x0A") - count)
                            except (ValueError, Exception) as e:
                                wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)

                            text = text + one_text
                            break
                    else:
                        pass

                    time.sleep(0.01)

                wx.CallAfter(pub.sendMessage, "update", data = text)

                if (text == "Running ...\x0D\x0A"):
                    pass
                else:
                    continue

                count = 0
                text = ""
                while (
                        (count < len("Running finished.\x0D\x0A\x0D\x0A")) and
                        (self.event_run_seq.is_set() == True)
                ):
                    try:
                        in_waiting = self.serial_port.inWaiting()
                    except (IOError) as e:
                        print "Serial_read_thread.run in_waiting: " + e.message
                        wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)
                        continue

                    if (in_waiting > 0):
                        if ((count + in_waiting) <= len("Running finished.\x0D\x0A\x0D\x0A")):
                            #print in_waiting
                            try:
                                one_text = self.serial_port.read(in_waiting)
                            except (ValueError, Exception) as e:
                                wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)

                            text = text + one_text
                            count = count + in_waiting
                        else:
                            try:
                                one_text = self.serial_port.read(len("Running finished.\x0D\x0A\x0D\x0A") - count)
                            except (ValueError, Exception) as e:
                                wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)

                            text = text + one_text
                            break
                    else:
                        pass

                    time.sleep(0.01)

                wx.CallAfter(pub.sendMessage, "update", data = text)

                if (text == "Running finished.\x0D\x0A\x0D\x0A"):
                    self.event_run_finished.set()
                else:
                    continue
            else:
                try:
                    in_waiting = self.serial_port.inWaiting()
                except (IOError) as e:
                    print "Serial_read_thread.run in_waiting: " + e.message
                    continue

                if (in_waiting > 0):
                    try:
                        text = self.serial_port.read(in_waiting)
                        #print type(text)
                    except (ValueError, Exception) as e:
                        wx.CallAfter(pub.sendMessage, "serial_read_error", data = e.message)
                    else:
                        wx.CallAfter(pub.sendMessage, "update", data = text)
                else:
                    pass

            # This is necessary, or it cost huge CPU
            time.sleep(0.01)
