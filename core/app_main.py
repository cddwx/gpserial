#!/usr/bin/env python
# coding=utf-8

import wx

from wx.lib.pubsub import pub
from serial import Serial

from serial_thread import serial_thread
from app_frame import app_frame


class app_main(wx.App):
    def OnInit(self):
        self.ser = Serial()

        self.thread = serial_thread(self.ser)

        self.frame = app_frame(self.ser)
        pub.subscribe(self.frame.on_recieve_area_update, "update")
        self.frame.Show()

        return True

    def OnExit(self):
        self.thread.stop()
