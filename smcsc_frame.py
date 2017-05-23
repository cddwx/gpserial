#!/usr/bin/env python
# coding=utf-8

import wx
from wx.lib import buttons

from smcsc_parameter import smcsc_parameter

class smcsc_frame(wx.Frame):
    def __init__(self, serial_obj, frame_title, com_choices):
        wx.Frame.__init__(
                self,
                parent=None,
                id=wx.ID_ANY,
                title=frame_title,
                pos=wx.DefaultPosition,
                size=wx.DefaultSize,
        )

        self.ser = serial_obj
        self.com_choices = com_choices

        panel = wx.Panel(self)

        # Recieve objects.
        self.m_recieve_title = wx.StaticText(panel, label=u"Recieve area")
        self.m_recieve_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.m_recieve_clear_button = wx.Button(panel, label=u"Clear")

        # Send objects.
        self.m_action_title = wx.StaticText(panel, label=u"Hex code send")

        self.m_action_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_HRULES)
        self.m_action_list.InsertColumn(0, u"Number", format=wx.LIST_FORMAT_LEFT)
        self.m_action_list.InsertColumn(1, u"Command", format=wx.LIST_FORMAT_LEFT)
        self.m_action_list.InsertColumn(2, u"Parameter", format=wx.LIST_FORMAT_LEFT)
        self.m_action_list.InsertColumn(3, u"Hex code", format=wx.LIST_FORMAT_LEFT)

        self.m_action_send_button = wx.Button(panel, label=u"Send")


        # Serial parameter setting.
        self.m_serial_title = wx.StaticText(panel, label=u"Serial port setting")

        self.m_serial_com_title = wx.StaticText(panel, label=u"Port: ")

        self.m_serial_com_select = wx.ComboBox(panel, choices=self.com_choices, style=wx.CB_READONLY)
        self.m_serial_com_select.SetSelection(0)

        self.m_serial_bitrate_title = wx.StaticText(panel, label=u"Bitrate: ")

        m_bitrate_choices = [ u"2400", u"4800", u"9600", u"14400", u"19200", u"28800", u"57600" ]
        self.m_serial_bitrate_select = wx.ComboBox(panel, choices=m_bitrate_choices, style=wx.CB_READONLY)
        self.m_serial_bitrate_select.SetSelection(2)


        self.m_serial_databit_title = wx.StaticText(panel, label=u"Databit: ")

        m_databit_choices = [ u"5", u"6", u"7", u"8" ]
        self.m_serial_databit_select = wx.ComboBox(panel, choices=m_databit_choices, style=wx.CB_READONLY)
        self.m_serial_databit_select.SetSelection(3)

        self.m_serial_checkbit_title = wx.StaticText(panel, label=u"Checkbit: ")

        m_checkbit_choices = [ u"None", u"Odd", u"Even", u"One", u"Zero" ]
        self.m_serial_checkbit_select = wx.ComboBox(panel, choices=m_checkbit_choices, style=wx.CB_READONLY)
        self.m_serial_checkbit_select.SetSelection(0)


        self.m_serial_stopbit_title = wx.StaticText(panel, label=u"Stopbit: ")

        m_stopbit_choices = [ u"1", u"2" ]
        self.m_serial_stopbit_select = wx.ComboBox(panel, choices=m_stopbit_choices, style=wx.CB_READONLY)
        self.m_serial_stopbit_select.SetSelection(0)

        self.m_serial_open_button = buttons.GenButton(panel, wx.ID_ANY, u"Open port")
        self.m_serial_open_button.Enable(True)

        self.m_serial_close_button = buttons.GenButton(panel, wx.ID_ANY, u"Close port")
        self.m_serial_close_button.Enable(False)

        # Program operation.
        self.m_program_exit_button = wx.Button(panel, label=u"Exit")


        #
        # Write area.
        #
        self.m_write_title = wx.StaticText(panel, label=u"Write commands")
        self.m_write_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.m_write_convert_button = wx.Button(panel, label=u"Convert to hex code")


        #
        # Arrangement.
        #
        recieve_area_box = wx.BoxSizer(wx.VERTICAL)
        recieve_area_box.Add(self.m_recieve_title, 0)
        recieve_area_box.Add(self.m_recieve_area, 1, wx.EXPAND)
        recieve_area_box.Add(self.m_recieve_clear_button, 0)

        setting_area_parameter_port_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_port_box.Add(self.m_serial_com_title, 1)
        setting_area_parameter_port_box.Add(self.m_serial_com_select, 1)

        setting_area_parameter_bitrate_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_bitrate_box.Add(self.m_serial_bitrate_title, 1)
        setting_area_parameter_bitrate_box.Add(self.m_serial_bitrate_select, 1)

        setting_area_parameter_databit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_databit_box.Add(self.m_serial_databit_title, 1)
        setting_area_parameter_databit_box.Add(self.m_serial_databit_select, 1)

        setting_area_parameter_checkbit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_checkbit_box.Add(self.m_serial_checkbit_title, 1)
        setting_area_parameter_checkbit_box.Add(self.m_serial_checkbit_select, 1)

        setting_area_parameter_stopbit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_stopbit_box.Add(self.m_serial_stopbit_title, 1)
        setting_area_parameter_stopbit_box.Add(self.m_serial_stopbit_select, 1)

        setting_area_parameter_box = wx.BoxSizer(wx.VERTICAL)
        setting_area_parameter_box.Add(setting_area_parameter_port_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_bitrate_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_databit_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_checkbit_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_stopbit_box, 1, wx.EXPAND)

        
        setting_area_operate_open_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_open_box.Add(self.m_serial_open_button, 0)

        setting_area_operate_close_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_close_box.Add(self.m_serial_close_button, 0)

        setting_area_operate_exit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_exit_box.Add(self.m_program_exit_button, 0)
        
        setting_area_operate_box = wx.BoxSizer(wx.VERTICAL)
        setting_area_operate_box.Add(setting_area_operate_open_box, 1, wx.ALIGN_CENTER)
        setting_area_operate_box.Add(setting_area_operate_close_box, 1, wx.ALIGN_CENTER)
        setting_area_operate_box.Add(setting_area_operate_exit_box, 1, wx.ALIGN_CENTER)

        setting_area_content_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_content_box.Add(setting_area_parameter_box, 1, wx.EXPAND)
        setting_area_content_box.Add(setting_area_operate_box, 1, wx.EXPAND)

        setting_area_box = wx.BoxSizer(wx.VERTICAL)
        setting_area_box.Add(self.m_serial_title, 0)
        setting_area_box.Add(setting_area_content_box, 1, wx.EXPAND)

        send_area_box = wx.BoxSizer(wx.VERTICAL)
        send_area_box.Add(self.m_action_title, 0)
        send_area_box.Add(self.m_action_list, 1, wx.EXPAND)
        send_area_box.Add(self.m_action_send_button, 0)
        
        write_area_box = wx.BoxSizer(wx.VERTICAL)
        write_area_box.Add(self.m_write_title, 0)
        write_area_box.Add(self.m_write_area, 1, wx.EXPAND)
        write_area_box.Add(self.m_write_convert_button, 0)
        
        up_box = wx.BoxSizer(wx.HORIZONTAL)
        up_box.Add(recieve_area_box, 1, wx.EXPAND | wx.ALL, 5)
        up_box.Add(setting_area_box, 1, wx.EXPAND | wx.ALL, 5)

        down_box = wx.BoxSizer(wx.HORIZONTAL)
        down_box.Add(send_area_box, 1, wx.EXPAND | wx.ALL, 5)
        down_box.Add(write_area_box, 1, wx.EXPAND | wx.ALL, 5)

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(up_box, 1, wx.EXPAND | wx.ALL, 5)
        main_box.Add(down_box, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_box)
        panel.Layout()
        panel.Fit()
        #panel.Centre()

        #self.SetSizer(main_vbox)
        self.Layout()
        self.Fit()
        #self.Centre()


        #
        # Connect Events
        #
        self.m_recieve_clear_button.Bind(wx.EVT_BUTTON, self.on_recieve_clear_button_clicked)

        self.m_serial_open_button.Bind(wx.EVT_BUTTON, self.on_serial_open_button_clicked)
        self.m_serial_close_button.Bind(wx.EVT_BUTTON, self.on_serial_close_button_clicked)
        self.m_program_exit_button.Bind(wx.EVT_BUTTON, self.on_program_exit_button_clicked)

        self.m_action_send_button.Bind(wx.EVT_BUTTON, self.on_action_send_button_clicked)

        self.m_write_convert_button.Bind(wx.EVT_BUTTON, self.on_write_convert_button_clicked)



    # Recieve area update
    def on_recieve_area_update(self, data):
        self.m_recieve_area.AppendText(data)


        # Recieve area.
    def on_recieve_clear_button_clicked(self, event):
        self.m_recieve_area.Clear()


    # Parameter setting area.
    def on_serial_open_button_clicked(self, event):
        if not self.ser.isOpen():
            try:
                self.ser.timeout = 1
                self.ser.xonxoff = 0
                self.ser.port = self.m_serial_com_select.GetValue()
                self.ser.parity = self.m_serial_checkbit_select.GetValue()[0]
                self.ser.baudrate = int(self.m_serial_bitrate_select.GetValue())
                self.ser.bytesize = int(self.m_serial_databit_select.GetValue())
                self.ser.stopbits = int(self.m_serial_stopbit_select.GetValue())
                self.ser.open()
            except Exception, e:
                print '[serial_frame\t] COMM Open Fail!', e

            else:
                self.m_serial_open_button.Enable(False)
                self.m_serial_close_button.Enable(True)
        else:
            pass


    def on_serial_close_button_clicked(self, event):
        if self.ser.isOpen():
            try:
                self.ser.close()
                while self.ser.isOpen():
                    pass

            except Exception, e:
                print '[serial_frame\t] COMM close Fail!', e

            else:
                self.m_serial_open_button.Enable(True)
                self.m_serial_close_button.Enable(False)

        else:
            pass


    # Program exit.
    def on_program_exit_button_clicked(self, event):
        self.Close()
        print "[serial_fram\t] Frame exit."
        #self.Destroy()


    def on_write_convert_button_clicked(self, event):
        self.m_action_list.ClearAll()
        parameter_converter = smcsc_parameter()
        
        command_text = self.m_write_area.GetValue()
        command_list = command_text.splitlines()
        action_index = 0
        for command in command_list:
            single_command_list = command.split()

            print single_command_list
            print action_index
            print parameter_converter.command(single_command_list)
            
            #self.m_action_list.InsertStringItem(action_index, str(action_index + 1))
            self.m_action_list.InsertStringItem(action_index, "hello")
            self.m_action_list.SetStringItem(action_index, 1, str(single_command_list[0]))
            self.m_action_list.SetStringItem(action_index, 2, str(single_command_list[1:]))
            self.m_action_list.SetStringItem(action_index, 3, str(parameter_converter.command(single_command_list)))
            self.m_action_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.m_action_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.m_action_list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
            self.m_action_list.SetColumnWidth(3, wx.LIST_AUTOSIZE)

            action_index =  action_index + 1


    def on_action_send_button_clicked(self, event):
        try:
            self.ser.write(''.join(real_commands).decode("hex"))
        except Exception, e:
            print '[smcsc_frame\t] Write Fail!', e

        else:
            print '[smcsc_frame\t] Write succeed!'