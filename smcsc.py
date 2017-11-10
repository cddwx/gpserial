#!/usr/bin/env python
# coding=utf-8

import wx

from main_frame import main_frame

class smcsc(wx.App):
    name    = u"SMCSC(Step motor control system client)"
    version = u"1.0"
    org     = u"OUYANG Lab"

    def OnInit(self):
        frame_title = self.name + "-" + self.version + " " + self.org

        self.frame = main_frame(frame_title)

        self.frame.Show()

        return True

if __name__ == "__main__":
    app = smcsc()
    app.MainLoop()
