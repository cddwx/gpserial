#!/usr/bin/env python
# coding=utf-8

from wx.lib.pubsub import pub
import wx

from serial import Serial

from smcsc_thread import smcsc_thread
from smcsc_frame import smcsc_frame


class smcsc_app(wx.App):
    def OnInit(self):
        self.ser = Serial()

        self.thread = smcsc_thread(self.ser)

        self.frame = smcsc_frame(self.ser)
        pub.subscribe(self.frame.on_recieve_area_update, "update")
        self.frame.Show()

        return True

    def OnExit(self):
        self.thread.stop()
