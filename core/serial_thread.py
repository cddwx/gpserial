#!/usr/bin/env python
# coding=utf-8

import time
import threading
import wx

from wx.lib.pubsub import pub

class serial_thread(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.event_stop = threading.Event()
        self.start()

    def run(self):
        while (not self.event_stop.is_set()):
            if self.ser.isOpen() and self.ser.inWaiting():
                text = self.ser.read(self.ser.inWaiting())
                wx.CallAfter(pub.sendMessage, "update", data=text)

            time.sleep(0.01)

    def stop(self):
        self.event_stop.set()
