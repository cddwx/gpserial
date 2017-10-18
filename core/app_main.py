#!/usr/bin/env python
# coding=utf-8

import wx

from main_window import main_window

class app_main(wx.App):
    def OnInit(self):
        frame_title = u"SMCSC-1.0 OUYANG Lab"

        self.frame = main_window(frame_title)

        self.frame.Show()

        return True

    def OnExit(self):
        pass
