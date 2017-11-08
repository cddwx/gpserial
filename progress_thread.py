#!/usr/bin/env python
# coding=utf-8

import time
import threading
import wx

from wx.lib.pubsub import pub

class progress_thread(threading.Thread):
    def __init__(self, max_count, tick):
        threading.Thread.__init__(self)

        self.max_count = max_count
        self.tick = tick

        self.event_stop = threading.Event()
        self.event_sync = threading.Event()

    def run(self):
        #dia = wx.ProgressDialog("Running", "Seq Running ..." , self.progress_max, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)

        count = 0
        while (count <= self.max_count):
            wx.CallAfter(pub.sendMessage, "progress_tick", data=count)
            time.sleep(1)

            if (self.event_sync.is_set() == True):
                count = self.tick
            else:
                count += 1
