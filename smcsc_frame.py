#!/usr/bin/env python
# coding=utf-8

import wx
from wx.lib import buttons

import serial.tools.list_ports

from smcsc_command_natural import smcsc_command_natural

class smcsc_frame(wx.Frame):
    def __init__(self, ser):
        wx.Frame.__init__(
                self,
                parent=None,
                id=wx.ID_ANY,
                title=u"Step motor control system client",
                pos=wx.DefaultPosition,
                size=wx.DefaultSize,
        )

        self.ser = ser

        self.parameter_converter = smcsc_command_natural()

        panel = wx.Panel(self)

        # Recieve objects.
        self.m_recieve_title = wx.StaticText(panel, label=u"Recieve area")
        self.m_recieve_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.m_recieve_clear_button = wx.Button(panel, label=u"Clear")

        # Send objects.
        self.m_action_title = wx.StaticText(panel, label=u"List command send")

        self.m_action_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        self.m_action_list.InsertColumn(0, u"Number", format=wx.LIST_FORMAT_LEFT)
        self.m_action_list.InsertColumn(1, u"Command", format=wx.LIST_FORMAT_LEFT)
        self.m_action_list.InsertColumn(2, u"Hex code", format=wx.LIST_FORMAT_LEFT)

        self.m_action_send_button = wx.Button(panel, label=u"Send")


        # Serial parameter setting.
        self.m_serial_title = wx.StaticText(panel, label=u"Serial port setting")

        self.m_serial_com_title = wx.StaticText(panel, label=u"Port: ")

        m_com_choices = self.get_m_com_choices()
        self.m_serial_com_select = wx.ComboBox(panel, choices=m_com_choices, style=wx.CB_READONLY)
        self.m_serial_com_select.SetSelection(0)

        self.m_serial_bitrate_title = wx.StaticText(panel, label=u"Bitrate: ")

        m_bitrate_choices = [ u"2400", u"4800", u"9600", u"14400", u"19200", u"28800", u"57600" ]
        self.m_serial_bitrate_select = wx.ComboBox(panel, choices=m_bitrate_choices, style=wx.CB_READONLY)
        self.m_serial_bitrate_select.SetValue(u"9600")


        self.m_serial_databit_title = wx.StaticText(panel, label=u"Databit: ")

        m_databit_choices = [ u"5", u"6", u"7", u"8" ]
        self.m_serial_databit_select = wx.ComboBox(panel, choices=m_databit_choices, style=wx.CB_READONLY)
        self.m_serial_databit_select.SetValue(u"8")

        self.m_serial_checkbit_title = wx.StaticText(panel, label=u"Checkbit: ")

        m_checkbit_choices = [ u"None", u"Odd", u"Even", u"One", u"Zero" ]
        self.m_serial_checkbit_select = wx.ComboBox(panel, choices=m_checkbit_choices, style=wx.CB_READONLY)
        self.m_serial_checkbit_select.SetValue(u"None")


        self.m_serial_stopbit_title = wx.StaticText(panel, label=u"Stopbit: ")

        m_stopbit_choices = [ u"1", u"2" ]
        self.m_serial_stopbit_select = wx.ComboBox(panel, choices=m_stopbit_choices, style=wx.CB_READONLY)
        self.m_serial_stopbit_select.SetValue(u"1")

        self.m_serial_check_button = wx.Button(panel, label=u"Check port")

        self.m_serial_open_button = buttons.GenButton(panel, label=u"Open port")
        self.m_serial_open_button.Enable(True)

        self.m_serial_close_button = buttons.GenButton(panel, label=u"Close port")
        self.m_serial_close_button.Enable(False)

        # Program operation.
        self.m_program_exit_button = wx.Button(panel, label=u"Exit")


        #
        # Write area.
        #
        self.m_write_title = wx.StaticText(panel, label=u"Write command list")
        self.m_write_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.m_write_convert_button = wx.Button(panel, label=u"Convert to hex code")

        self.m_send_title = wx.StaticText(panel, label=u"Write single command")
        self.m_send_input = wx.TextCtrl(panel)
        self.m_send_button = wx.Button(panel, label=u"Convert and send")

        self.m_constant_title = wx.StaticText(panel, label=u"Back code setting")

        self.m_direction_title = wx.StaticText(panel, label=u"Direction")
        self.m_direction_input = wx.TextCtrl(panel, value=self.parameter_converter.BACK_DIRECTION)

        self.m_interval_title = wx.StaticText(panel, label=u"Interval")
        self.m_interval_input = wx.TextCtrl(panel, value=self.parameter_converter.BACK_INTERVAL)

        self.m_step_count_title = wx.StaticText(panel, label=u"Step count")
        self.m_step_count_input = wx.TextCtrl(panel, value=self.parameter_converter.BACK_STEP_COUNT)

        self.m_pause_time_high_title = wx.StaticText(panel, label=u"Pause time high")
        self.m_pause_time_high_input = wx.TextCtrl(panel, value=self.parameter_converter.BACK_PAUSE_TIME_HIGH)

        self.m_pause_time_low_title = wx.StaticText(panel, label=u"Pause time low")
        self.m_pause_time_low_input = wx.TextCtrl(panel, value=self.parameter_converter.BACK_PAUSE_TIME_LOW)


        #
        # Connect Events
        #
        self.m_recieve_clear_button.Bind(wx.EVT_BUTTON, self.on_recieve_clear_button_clicked)

        self.m_serial_check_button.Bind(wx.EVT_BUTTON, self.on_serial_check_button_clicked)
        self.m_serial_open_button.Bind(wx.EVT_BUTTON, self.on_serial_open_button_clicked)
        self.m_serial_close_button.Bind(wx.EVT_BUTTON, self.on_serial_close_button_clicked)
        self.m_program_exit_button.Bind(wx.EVT_BUTTON, self.on_program_exit_button_clicked)

        self.m_action_send_button.Bind(wx.EVT_BUTTON, self.on_action_send_button_clicked)

        self.m_write_convert_button.Bind(wx.EVT_BUTTON, self.on_write_convert_button_clicked)
        self.m_send_button.Bind(wx.EVT_BUTTON, self.on_send_button_clicked)


        #
        # Arrangement.
        #

        # recieve_area_box
        recieve_area_box = wx.BoxSizer(wx.VERTICAL)
        recieve_area_box.Add(self.m_recieve_title, 0)
        recieve_area_box.Add(self.m_recieve_area, 1, wx.EXPAND)
        recieve_area_box.Add(self.m_recieve_clear_button, 0)

        setting_area_parameter_port_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_port_box.Add(self.m_serial_com_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_port_box.Add(self.m_serial_com_select, 1, wx.ALIGN_CENTER_VERTICAL)

        setting_area_parameter_bitrate_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_bitrate_box.Add(self.m_serial_bitrate_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_bitrate_box.Add(self.m_serial_bitrate_select, 1, wx.ALIGN_CENTER_VERTICAL)

        setting_area_parameter_databit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_databit_box.Add(self.m_serial_databit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_databit_box.Add(self.m_serial_databit_select, 1, wx.ALIGN_CENTER_VERTICAL)

        setting_area_parameter_checkbit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_checkbit_box.Add(self.m_serial_checkbit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_checkbit_box.Add(self.m_serial_checkbit_select, 1, wx.ALIGN_CENTER_VERTICAL)

        setting_area_parameter_stopbit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_stopbit_box.Add(self.m_serial_stopbit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_stopbit_box.Add(self.m_serial_stopbit_select, 1, wx.ALIGN_CENTER_VERTICAL)

        # setting_area_parameter_box
        setting_area_parameter_box = wx.BoxSizer(wx.VERTICAL)
        setting_area_parameter_box.Add(setting_area_parameter_port_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_bitrate_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_databit_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_checkbit_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_stopbit_box, 1, wx.EXPAND)


        setting_area_operate_check_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_check_box.Add(self.m_serial_check_button, 0, wx.ALIGN_CENTER_VERTICAL)

        setting_area_operate_open_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_open_box.Add(self.m_serial_open_button, 0, wx.ALIGN_CENTER_VERTICAL)

        setting_area_operate_close_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_close_box.Add(self.m_serial_close_button, 0, wx.ALIGN_CENTER_VERTICAL)

        setting_area_operate_exit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_exit_box.Add(self.m_program_exit_button, 0, wx.ALIGN_CENTER_VERTICAL)
        
        # setting_area_operate_box
        setting_area_operate_box = wx.BoxSizer(wx.VERTICAL)
        setting_area_operate_box.Add(setting_area_operate_check_box, 1, wx.ALIGN_CENTER)
        setting_area_operate_box.Add(setting_area_operate_open_box, 1, wx.ALIGN_CENTER)
        setting_area_operate_box.Add(setting_area_operate_close_box, 1, wx.ALIGN_CENTER)
        setting_area_operate_box.Add(setting_area_operate_exit_box, 1, wx.ALIGN_CENTER)

        # setting_area_content_box
        setting_area_content_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_content_box.Add(setting_area_parameter_box, 2, wx.EXPAND)
        setting_area_content_box.Add(setting_area_operate_box, 1, wx.EXPAND)

        # setting_area_box
        setting_area_box = wx.BoxSizer(wx.VERTICAL)
        setting_area_box.Add(self.m_serial_title, 0)
        setting_area_box.Add(setting_area_content_box, 1, wx.EXPAND)

        # send_area_box
        send_area_box = wx.BoxSizer(wx.VERTICAL)
        send_area_box.Add(self.m_action_title, 0)
        send_area_box.Add(self.m_action_list, 1, wx.EXPAND)
        send_area_box.Add(self.m_action_send_button, 0)


        # write_area_write_box
        write_area_write_box = wx.BoxSizer(wx.VERTICAL)
        write_area_write_box.Add(self.m_write_title, 0)
        write_area_write_box.Add(self.m_write_area, 1, wx.EXPAND)
        write_area_write_box.Add(self.m_write_convert_button, 0)
        write_area_write_box.Add(self.m_send_title, 0, wx.TOP, 10)
        write_area_write_box.Add(self.m_send_input, 0, wx.EXPAND)
        write_area_write_box.Add(self.m_send_button, 0)


        '''
        write_area_setting_direction_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_direction_box.Add(self.m_direction_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_direction_box.Add(self.m_direction_input, 1, wx.ALIGN_CENTER_VERTICAL)

        write_area_setting_interval_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_interval_box.Add(self.m_interval_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_interval_box.Add(self.m_interval_input, 1, wx.ALIGN_CENTER_VERTICAL)

        write_area_setting_step_count_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_step_count_box.Add(self.m_step_count_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_step_count_box.Add(self.m_step_count_input, 1, wx.ALIGN_CENTER_VERTICAL)

        write_area_setting_pause_time_high_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_pause_time_high_box.Add(self.m_pause_time_high_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_pause_time_high_box.Add(self.m_pause_time_high_input, 1, wx.ALIGN_CENTER_VERTICAL)

        write_area_setting_pause_time_low_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_pause_time_low_box.Add(self.m_pause_time_low_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_pause_time_low_box.Add(self.m_pause_time_low_input, 1, wx.ALIGN_CENTER_VERTICAL)
        '''

        # write_area_setting_box
        write_area_setting_box = wx.BoxSizer(wx.VERTICAL)
        write_area_setting_box.Add(self.m_constant_title, 0, wx.BOTTOM, 5)
        '''
        write_area_setting_box.Add(write_area_setting_direction_box, 1, wx.EXPAND)
        write_area_setting_box.Add(write_area_setting_interval_box, 1, wx.EXPAND)
        write_area_setting_box.Add(write_area_setting_step_count_box, 1, wx.EXPAND)
        write_area_setting_box.Add(write_area_setting_pause_time_high_box, 1, wx.EXPAND)
        write_area_setting_box.Add(write_area_setting_pause_time_low_box, 1, wx.EXPAND)
        '''
        write_area_setting_box.Add(self.m_direction_title, 0)
        write_area_setting_box.Add(self.m_direction_input, 0, wx.EXPAND | wx.BOTTOM, 5)
        write_area_setting_box.Add(self.m_interval_title, 0)
        write_area_setting_box.Add(self.m_interval_input, 0, wx.EXPAND | wx.BOTTOM, 5)
        write_area_setting_box.Add(self.m_step_count_title, 0)
        write_area_setting_box.Add(self.m_step_count_input, 0, wx.EXPAND | wx.BOTTOM, 5)
        write_area_setting_box.Add(self.m_pause_time_high_title, 0)
        write_area_setting_box.Add(self.m_pause_time_high_input, 0, wx.EXPAND | wx.BOTTOM, 5)
        write_area_setting_box.Add(self.m_pause_time_low_title, 0)
        write_area_setting_box.Add(self.m_pause_time_low_input, 0, wx.EXPAND | wx.BOTTOM, 5)

        # write_area_content_box
        write_area_content_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_content_box.Add(write_area_write_box, 3, wx.EXPAND)
        write_area_content_box.Add(write_area_setting_box, 2, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

        # write_area_box
        write_area_box = wx.BoxSizer(wx.VERTICAL)
        write_area_box.Add(write_area_content_box, 1, wx.EXPAND)

        # up_box
        up_box = wx.BoxSizer(wx.HORIZONTAL)
        up_box.Add(setting_area_box, 1, wx.EXPAND | wx.ALL, 5)
        up_box.Add(recieve_area_box, 2, wx.EXPAND | wx.ALL, 5)

        # down_box
        down_box = wx.BoxSizer(wx.HORIZONTAL)
        down_box.Add(write_area_box, 1, wx.EXPAND | wx.ALL, 5)
        down_box.Add(send_area_box, 2, wx.EXPAND | wx.ALL, 5)

        # main_box
        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(up_box, 1, wx.EXPAND | wx.ALL, 5)
        main_box.Add(down_box, 2, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_box)
        panel.Layout()
        panel.Fit()
        #panel.Centre()

        #self.SetSizer(main_vbox)
        self.Layout()
        self.Fit()
        #self.Centre()


    #
    # Assistant functions
    #
    def get_m_com_choices(self):
        m_com_choices = []
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) > 0:
            for port in port_list:
                m_com_choices.append(port[0])
        else:
            m_com_choices = []

        return m_com_choices

    def is_int(self, string):
        try:
            int(string)
            return True

        except ValueError:
            return False

    def is_hex(self, string):
        try:
            int(string, 16)
            return True

        except ValueError:
            return False

    def is_one_bit_hex(self, name, string):
        if (len(string) != 1):
            raise ValueError(name + " length is wrong! Need to be 1 bit.")

        if (not self.is_hex(string)):
            raise ValueError(name + " is not hex string!")

        if ((int(string, 16) < 0) or (int(string, 16) > 15)):
            raise ValueError(name + " is exced the range 0--F!")

        return True

    def is_two_bit_hex(self, name, string):
        if (len(string) != 2):
            raise ValueError(name + " length is wrong! Need to be 2 bit.")

        if (not self.is_hex(string)):
            raise ValueError(name + " is not hex string!")

        if ((int(string, 16) < 0) or (int(string, 16) > 255)):
            raise ValueError(name + " is exced the range 00--FF!")

        return True

    def set_constant(self):
        direction = str(self.m_direction_input.GetValue())
        interval = str(self.m_interval_input.GetValue())
        step_count = str(self.m_step_count_input.GetValue())
        pause_time_high = str(self.m_pause_time_high_input.GetValue())
        pause_time_low = str(self.m_pause_time_low_input.GetValue())

        try:
            if self.is_one_bit_hex("Direction", direction):
                self.parameter_converter.BACK_DIRECTION = direction

            if self.is_one_bit_hex("Interval", interval):
                self.parameter_converter.BACK_INTERVAL = interval

            if self.is_two_bit_hex("Step count", step_count):
                self.parameter_converter.BACK_STEP_COUNT = step_count

            if self.is_two_bit_hex("Pause time high", pause_time_high):
                self.parameter_converter.BACK_PAUSE_TIME_HIGH = pause_time_high

            if self.is_two_bit_hex("Pause time low", pause_time_low):
                self.parameter_converter.BACK_PAUSE_TIME_LOW = pause_time_low

        except ValueError as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    #
    # Event handle functions
    #

    # Recieve area update
    def on_recieve_area_update(self, data):
        #print "[data", data, "]"
        self.m_recieve_area.AppendText(data)


    # Recieve area.
    def on_recieve_clear_button_clicked(self, event):
        self.m_recieve_area.Clear()


    # Parameter setting area.
    def on_serial_check_button_clicked(self, event):
        self.m_serial_com_select.Set(self.get_m_com_choices())
        self.m_serial_com_select.SetSelection(0)


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

            except Exception as e:
                dia = wx.MessageDialog(None, "COMM Open Fail!\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
                dia.ShowModal()
                dia.Destroy()

                return

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

            except Exception as e:
                dia = wx.MessageDialog(None, "COMM close Fail!\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
                dia.ShowModal()
                dia.Destroy()

                return

            else:
                self.m_serial_open_button.Enable(True)
                self.m_serial_close_button.Enable(False)

        else:
            pass


    # Program exit.
    def on_program_exit_button_clicked(self, event):
        self.Close()


    def on_write_convert_button_clicked(self, event):
        if (self.m_write_area.GetValue() == ""):
            dia = wx.MessageDialog(None, "Command list is empty!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        command_string_list = str(self.m_write_area.GetValue()).splitlines()

        line_number = 1
        for command_string in command_string_list:
            try:
                command = command_string.split()
                code = self.parameter_converter.convert(command)

            except Exception as e:
                dia = wx.MessageDialog(None, "Command Error in line: " + str(line_number) + "\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
                dia.ShowModal()
                dia.Destroy()

                return

            line_number = line_number + 1

        self.m_action_list.DeleteAllItems()
        self.set_constant()

        action_index = 0
        for command_string in command_string_list:
            command = command_string.split()

            #print "[command: ", command, "]"

            self.m_action_list.InsertStringItem(action_index, str(action_index + 1))
            self.m_action_list.SetStringItem(action_index, 1, str(" ".join(command)))
            self.m_action_list.SetStringItem(action_index, 2, str(" ".join(self.parameter_converter.convert(command))))
            self.m_action_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.m_action_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.m_action_list.SetColumnWidth(2, wx.LIST_AUTOSIZE)

            action_index =  action_index + 1


    def on_action_send_button_clicked(self, event):
        if (self.m_action_list.GetItemCount() == 0):
            dia = wx.MessageDialog(None, "The item list is empty!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        if (self.m_action_list.GetFirstSelected() == -1):
            dia = wx.MessageDialog(None, "No item is selected!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        try:
            action_index = self.m_action_list.GetFirstSelected()
            code = str(self.m_action_list.GetItemText(action_index, 2)).split()

            #print "[code: ", code, "]"

            self.ser.write("".join(code).decode("hex"))

        except Exception as e:
            dia = wx.MessageDialog(None, "Write Failed!\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    def on_send_button_clicked(self, event):
        try:
            self.set_constant()
            command = str(self.m_send_input.GetValue()).split()
            code = self.parameter_converter.convert(command)

            #print "[command: ", command, "]"
            #print "[code: ", code, "]"

        except Exception as e:
            dia = wx.MessageDialog(None, "Send failed!\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        try:
            self.ser.write("".join(code).decode("hex"))

        except Exception as e:
            dia = wx.MessageDialog(None, "Write Failed!\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return
