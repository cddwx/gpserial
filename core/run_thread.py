#!/usr/bin/env python
# coding=utf-8

import time
import threading
import wx

from wx.lib.pubsub import pub

class run_thread(threading.Thread):
    def __init__(self, serial_port, serial_read_thread, code_list):
        threading.Thread.__init__(self)

        self.serial_port = serial_port
        self.serial_read_thread = serial_read_thread
        self.code_list = code_list

        self.event_stop = threading.Event()

    def run(self):
        self.serial_read_thread.event_run_seq.set()

        for code in self.code_list:
            if (self.event_stop.is_set()):
                self.serial_read_thread.event_run_seq.clear()
                wx.CallAfter(pub.sendMessage, "run_seq_finished", data = "OK")

                return
            else:
                try:
                    self.serial_port.write("".join(code).decode("hex"))
                except (ValueError, Exception) as e:
                    self.serial_read_thread.event_run_seq.clear()
                    wx.CallAfter(pub.sendMessage, "run_write_error", data = e.message)
                    wx.CallAfter(pub.sendMessage, "run_seq_finished", data = "OK")

                    return

                #print code
                self.serial_read_thread.event_run_finished.wait()
                self.serial_read_thread.event_run_finished.clear()

        self.serial_read_thread.event_run_seq.clear()
        wx.CallAfter(pub.sendMessage, "run_seq_finished", data = "OK")
