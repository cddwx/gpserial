#!/usr/bin/env python
# coding=utf-8

import time
import wx

from wx.lib.pubsub import pub
from serial import Serial
from serial.tools.list_ports import comports

from command_converter import command_converter
from run_thread import run_thread
from serial_read_thread import serial_read_thread

class main_window(wx.Frame):
    ############################################################################
    # Init
    ############################################################################
    def __init__(self, frame_title):
        wx.Frame.__init__(
                self,
                parent = None,
                id = wx.ID_ANY,
                title = frame_title,
                pos = wx.DefaultPosition,
                size = wx.DefaultSize,
        )

        self.serial_port = Serial()
        self.converter = command_converter()


        self.create_objects()
        self.connect_events()
        self.arrange_objects()


        pub.subscribe(self.on_recieve_area_update, "update")
        pub.subscribe(self.on_serial_read_error, "serial_read_error")
        pub.subscribe(self.on_run_write_error, "run_write_error")
        pub.subscribe(self.on_run_seq_finished, "run_seq_finished")


    ###########################################################################
    # Create objects
    ###########################################################################
    def create_objects(self):
        self.panel = wx.Panel(self)

        #
        # Recieve objects.
        #
        self.m_recieve_title = wx.StaticText(self.panel, label=u"Recieve area")
        self.m_recieve_area = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.m_recieve_clear_button = wx.Button(self.panel, label=u"Clear")

        #
        # Send objects.
        #
        self.m_action_title = wx.StaticText(self.panel, label=u"List command/code")

        self.m_action_list = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        self.m_action_list.InsertColumn(0, u"Id", format=wx.LIST_FORMAT_LEFT)
        self.m_action_list.InsertColumn(1, u"Command", format=wx.LIST_FORMAT_LEFT)
        self.m_action_list.InsertColumn(2, u"Hex code", format=wx.LIST_FORMAT_LEFT)

        self.m_action_send_button = wx.Button(self.panel, label=u"Send")
        self.m_action_send_next_button = wx.Button(self.panel, label=u"Send next")


        #
        # Serial parameter setting.
        #
        self.m_serial_title = wx.StaticText(self.panel, label=u"Serial port setting")

        self.m_serial_com_title = wx.StaticText(self.panel, label=u"Port: ")

        m_com_choices = self.get_m_com_choices()
        self.m_serial_com_select = wx.ComboBox(self.panel, choices=m_com_choices, style=wx.CB_READONLY)
        self.m_serial_com_select.SetSelection(0)

        self.m_serial_bitrate_title = wx.StaticText(self.panel, label=u"Bitrate: ")

        m_bitrate_choices = [ u"2400", u"4800", u"9600", u"14400", u"19200", u"28800", u"57600" ]
        self.m_serial_bitrate_select = wx.ComboBox(self.panel, choices=m_bitrate_choices, style=wx.CB_READONLY)
        self.m_serial_bitrate_select.SetValue(u"9600")


        self.m_serial_databit_title = wx.StaticText(self.panel, label=u"Databit: ")

        m_databit_choices = [ u"5", u"6", u"7", u"8" ]
        self.m_serial_databit_select = wx.ComboBox(self.panel, choices=m_databit_choices, style=wx.CB_READONLY)
        self.m_serial_databit_select.SetValue(u"8")

        self.m_serial_checkbit_title = wx.StaticText(self.panel, label=u"Checkbit: ")

        m_checkbit_choices = [ u"None", u"Odd", u"Even", u"One", u"Zero" ]
        self.m_serial_checkbit_select = wx.ComboBox(self.panel, choices=m_checkbit_choices, style=wx.CB_READONLY)
        self.m_serial_checkbit_select.SetValue(u"None")


        self.m_serial_stopbit_title = wx.StaticText(self.panel, label=u"Stopbit: ")

        m_stopbit_choices = [ u"1", u"2" ]
        self.m_serial_stopbit_select = wx.ComboBox(self.panel, choices=m_stopbit_choices, style=wx.CB_READONLY)
        self.m_serial_stopbit_select.SetValue(u"1")

        self.m_serial_check_button = wx.Button(self.panel, label=u"Check port")

        self.m_serial_open_button = wx.Button(self.panel, label=u"Open port")
        self.m_serial_open_button.Enable(True)

        self.m_serial_close_button = wx.Button(self.panel, label=u"Close port")
        self.m_serial_close_button.Enable(False)

        # Program operation.
        self.m_program_exit_button = wx.Button(self.panel, label=u"Exit")


        #
        # Write area.
        #
        self.m_write_title = wx.StaticText(self.panel, label=u"Command seq")
        self.m_write_area = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.m_write_convert_button     = wx.Button(self.panel, label=u"Check seq")
        self.m_write_run_seq_button     = wx.Button(self.panel, label=u"Run seq")
        self.m_write_run_seq_button.Enable(False)
        self.m_write_stop_seq_button     = wx.Button(self.panel, label=u"Stop seq")
        self.m_write_stop_seq_button.Enable(False)

        self.m_write_reset_button     = wx.Button(self.panel, label=u"*** MCU RESET ***")
        self.m_write_command_reset_button       = wx.Button(self.panel, label=u"Command reset")
        self.m_write_run_button         = wx.Button(self.panel, label=u"= Run code =")
        self.m_write_show_ram_button    = wx.Button(self.panel, label=u"Show RAM code")
        self.m_write_show_eeprom_button = wx.Button(self.panel, label=u"Show EEPROM code")
        self.m_write_write_button       = wx.Button(self.panel, label=u"Write to EEPROM")
        self.m_write_read_button        = wx.Button(self.panel, label=u"Load from EEPROM")

        self.m_send_title = wx.StaticText(self.panel, label=u"Single command/code")
        self.m_send_input = wx.TextCtrl(self.panel, value=u"")
        self.m_send_button = wx.Button(self.panel, label=u"Send command")
        self.m_send_hex_button = wx.Button(self.panel, label=u"Send code")


        '''
        self.m_back_code_setting_title = wx.StaticText(self.panel, label=u"Back code setting")

        self.m_direction_title = wx.StaticText(self.panel, label=u"Back direction")
        self.m_direction_input = wx.TextCtrl(self.panel, value=self.converter.BACK_DIRECTION)

        self.m_interval_title = wx.StaticText(self.panel, label=u"Back interval")
        self.m_interval_input = wx.TextCtrl(self.panel, value=self.converter.BACK_INTERVAL)

        self.m_step_count_title = wx.StaticText(self.panel, label=u"Back step count")
        self.m_step_count_input = wx.TextCtrl(self.panel, value=self.converter.BACK_STEP_COUNT)

        self.m_pause_time_high_title = wx.StaticText(self.panel, label=u"Back pause time high")
        self.m_pause_time_high_input = wx.TextCtrl(self.panel, value=self.converter.BACK_PAUSE_TIME_HIGH)

        self.m_pause_time_low_title = wx.StaticText(self.panel, label=u"Back pause time low")
        self.m_pause_time_low_input = wx.TextCtrl(self.panel, value=self.converter.BACK_PAUSE_TIME_LOW)
        '''



    ############################################################################
    # Connect Events
    ############################################################################
    def connect_events(self):
        self.m_recieve_clear_button.Bind(wx.EVT_BUTTON, self.on_recieve_clear_button_clicked)

        self.m_serial_check_button.Bind(wx.EVT_BUTTON, self.on_serial_check_button_clicked)
        self.m_serial_open_button.Bind(wx.EVT_BUTTON, self.on_serial_open_button_clicked)
        self.m_serial_close_button.Bind(wx.EVT_BUTTON, self.on_serial_close_button_clicked)
        self.m_program_exit_button.Bind(wx.EVT_BUTTON, self.on_program_exit_button_clicked)

        self.m_action_send_button.Bind(wx.EVT_BUTTON, self.on_action_send_button_clicked)
        self.m_action_send_next_button.Bind(wx.EVT_BUTTON, self.on_action_send_next_button_clicked)

        self.m_write_convert_button.Bind(wx.EVT_BUTTON, self.on_write_convert_button_clicked)
        self.m_write_run_seq_button.Bind(wx.EVT_BUTTON, self.on_write_run_seq_button_clicked)
        self.m_write_stop_seq_button.Bind(wx.EVT_BUTTON, self.on_write_stop_seq_button_clicked)
        self.m_write_reset_button.Bind(wx.EVT_BUTTON, self.on_write_reset_button_clicked)
        self.m_write_command_reset_button.Bind(wx.EVT_BUTTON, self.on_write_command_reset_button_clicked)
        self.m_write_run_button.Bind(wx.EVT_BUTTON, self.on_write_run_button_clicked)
        self.m_write_show_ram_button.Bind(wx.EVT_BUTTON, self.on_write_show_ram_button_clicked)
        self.m_write_show_eeprom_button.Bind(wx.EVT_BUTTON, self.on_write_show_eeprom_button_clicked)
        self.m_write_write_button.Bind(wx.EVT_BUTTON, self.on_write_write_button_clicked)
        self.m_write_read_button.Bind(wx.EVT_BUTTON, self.on_write_read_button_clicked)

        self.m_send_button.Bind(wx.EVT_BUTTON, self.on_send_button_clicked)
        self.m_send_hex_button.Bind(wx.EVT_BUTTON, self.on_send_hex_button_clicked)



    ############################################################################
    # Arrange objects.
    # I find it is more confortable to arrange from big to small.
    ############################################################################
    def arrange_objects(self):
        # setting_area-content-parameter-port
        setting_area_parameter_port_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_port_box.Add(self.m_serial_com_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_port_box.Add(self.m_serial_com_select, 1, wx.ALIGN_CENTER_VERTICAL)

        # setting_area-content-parameter-bitrate
        setting_area_parameter_bitrate_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_bitrate_box.Add(self.m_serial_bitrate_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_bitrate_box.Add(self.m_serial_bitrate_select, 1, wx.ALIGN_CENTER_VERTICAL)

        # setting_area-content-parameter-databit
        setting_area_parameter_databit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_databit_box.Add(self.m_serial_databit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_databit_box.Add(self.m_serial_databit_select, 1, wx.ALIGN_CENTER_VERTICAL)

        # setting_area-content-parameter-checkbit
        setting_area_parameter_checkbit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_checkbit_box.Add(self.m_serial_checkbit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_checkbit_box.Add(self.m_serial_checkbit_select, 1, wx.ALIGN_CENTER_VERTICAL)

        # setting_area-content-parameter-stopbit
        setting_area_parameter_stopbit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_parameter_stopbit_box.Add(self.m_serial_stopbit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        setting_area_parameter_stopbit_box.Add(self.m_serial_stopbit_select, 1, wx.ALIGN_CENTER_VERTICAL)

        # setting_area-content-parameter
        setting_area_parameter_box = wx.BoxSizer(wx.VERTICAL)
        setting_area_parameter_box.Add(setting_area_parameter_port_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_bitrate_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_databit_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_checkbit_box, 1, wx.EXPAND)
        setting_area_parameter_box.Add(setting_area_parameter_stopbit_box, 1, wx.EXPAND)


        # setting_area-content-operate-check
        setting_area_operate_check_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_check_box.Add(self.m_serial_check_button, 0, wx.ALIGN_CENTER_VERTICAL)

        # setting_area-content-operate-open
        setting_area_operate_open_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_open_box.Add(self.m_serial_open_button, 0, wx.ALIGN_CENTER_VERTICAL)

        # setting_area-content-operate-close
        setting_area_operate_close_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_close_box.Add(self.m_serial_close_button, 0, wx.ALIGN_CENTER_VERTICAL)

        # setting_area-content-operate-exit
        setting_area_operate_exit_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_operate_exit_box.Add(self.m_program_exit_button, 0, wx.ALIGN_CENTER_VERTICAL)
        
        # setting_area-content-operate
        setting_area_operate_box = wx.BoxSizer(wx.VERTICAL)
        setting_area_operate_box.Add(setting_area_operate_check_box, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        setting_area_operate_box.Add(setting_area_operate_open_box, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        setting_area_operate_box.Add(setting_area_operate_close_box, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        setting_area_operate_box.Add(setting_area_operate_exit_box, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        # setting_area-content
        setting_area_content_box = wx.BoxSizer(wx.HORIZONTAL)
        setting_area_content_box.Add(setting_area_parameter_box, 2, wx.EXPAND)
        setting_area_content_box.Add(setting_area_operate_box, 1, wx.EXPAND)

        # setting_area
        setting_area_box = wx.BoxSizer(wx.VERTICAL)
        setting_area_box.Add(self.m_serial_title, 0)
        setting_area_box.Add(setting_area_content_box, 1, wx.EXPAND)


        '''
        # write_area-setting-direction
        write_area_setting_direction_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_direction_box.Add(self.m_direction_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_direction_box.Add(self.m_direction_input, 1, wx.ALIGN_CENTER_VERTICAL)

        # write_area-setting-interval
        write_area_setting_interval_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_interval_box.Add(self.m_interval_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_interval_box.Add(self.m_interval_input, 1, wx.ALIGN_CENTER_VERTICAL)

        # write_area-setting-step_count
        write_area_setting_step_count_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_step_count_box.Add(self.m_step_count_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_step_count_box.Add(self.m_step_count_input, 1, wx.ALIGN_CENTER_VERTICAL)

        # write_area-setting-pause_time_high
        write_area_setting_pause_time_high_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_pause_time_high_box.Add(self.m_pause_time_high_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_pause_time_high_box.Add(self.m_pause_time_high_input, 1, wx.ALIGN_CENTER_VERTICAL)

        # write_area-setting-pause_time_low
        write_area_setting_pause_time_low_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_setting_pause_time_low_box.Add(self.m_pause_time_low_title, 1, wx.ALIGN_CENTER_VERTICAL)
        write_area_setting_pause_time_low_box.Add(self.m_pause_time_low_input, 1, wx.ALIGN_CENTER_VERTICAL)

        # write_area-setting
        write_area_setting_box = wx.BoxSizer(wx.VERTICAL)
        write_area_setting_box.Add(self.m_back_code_setting_title, 0)
        write_area_setting_box.Add(write_area_setting_direction_box, 0, wx.EXPAND)
        write_area_setting_box.Add(write_area_setting_interval_box, 0, wx.EXPAND)
        write_area_setting_box.Add(write_area_setting_step_count_box, 0, wx.EXPAND)
        write_area_setting_box.Add(write_area_setting_pause_time_high_box, 0, wx.EXPAND)
        write_area_setting_box.Add(write_area_setting_pause_time_low_box, 0, wx.EXPAND)
        '''


        # write_area-seq_buttons
        write_area_seq_buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_seq_buttons_box.Add(self.m_write_convert_button, 1, wx.ALL, 5)
        write_area_seq_buttons_box.Add(self.m_write_run_seq_button, 1, wx.ALL, 5)
        write_area_seq_buttons_box.Add(self.m_write_stop_seq_button, 1, wx.ALL, 5)


        # write_area-buttons2
        write_area_buttons2_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_buttons2_box.Add(self.m_write_command_reset_button, 1, wx.ALL, 5)
        write_area_buttons2_box.Add(self.m_write_run_button, 1, wx.ALL, 5)

        # write_area-buttons3
        write_area_buttons3_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_buttons3_box.Add(self.m_write_show_ram_button, 1, wx.ALL, 5)
        write_area_buttons3_box.Add(self.m_write_show_eeprom_button, 1, wx.ALL, 5)

        # write_area-buttons4
        write_area_buttons4_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_buttons4_box.Add(self.m_write_write_button, 1, wx.ALL, 5)
        write_area_buttons4_box.Add(self.m_write_read_button, 1, wx.ALL, 5)

        # write_area-send_buttons
        write_area_send_buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        write_area_send_buttons_box.Add(self.m_send_button, 1, wx.ALL, 5)
        write_area_send_buttons_box.Add(self.m_send_hex_button, 1, wx.ALL, 5)


        # write_area-write
        write_area_write_box = wx.BoxSizer(wx.VERTICAL)
        write_area_write_box.Add(self.m_write_title, 0, wx.TOP, 10)
        write_area_write_box.Add(self.m_write_area, 1, wx.EXPAND)
        write_area_write_box.Add(write_area_seq_buttons_box, 0, wx.EXPAND)
        write_area_write_box.Add(self.m_write_reset_button, 0, wx.EXPAND | wx.ALL, 5)
        write_area_write_box.Add(write_area_buttons2_box, 0, wx.EXPAND)
        write_area_write_box.Add(write_area_buttons3_box, 0, wx.EXPAND)
        write_area_write_box.Add(write_area_buttons4_box, 0, wx.EXPAND)
        write_area_write_box.Add(self.m_send_title, 0, wx.TOP, 10)
        write_area_write_box.Add(self.m_send_input, 0, wx.EXPAND)
        write_area_write_box.Add(write_area_send_buttons_box, 0, wx.EXPAND)

        # write_area
        write_area_box = wx.BoxSizer(wx.VERTICAL)
        #write_area_box.Add(write_area_setting_box, 0, wx.EXPAND)
        write_area_box.Add(write_area_write_box, 1, wx.EXPAND)


        # recieve_area
        recieve_area_box = wx.BoxSizer(wx.VERTICAL)
        recieve_area_box.Add(self.m_recieve_title, 0)
        recieve_area_box.Add(self.m_recieve_area, 1, wx.EXPAND)
        recieve_area_box.Add(self.m_recieve_clear_button, 0, wx.ALL, 5)


        # send_area-operate
        send_area_operate_box = wx.BoxSizer(wx.HORIZONTAL)
        send_area_operate_box.Add(self.m_action_send_button, 1, wx.ALL, 5)
        send_area_operate_box.Add(self.m_action_send_next_button, 1, wx.ALL, 5)

        # send_area
        send_area_box = wx.BoxSizer(wx.VERTICAL)
        send_area_box.Add(self.m_action_title, 0)
        send_area_box.Add(self.m_action_list, 1, wx.EXPAND)
        send_area_box.Add(send_area_operate_box, 0, wx.EXPAND)


        # left
        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(setting_area_box, 2, wx.EXPAND | wx.ALL, 5)
        left_box.Add(write_area_box, 5, wx.EXPAND | wx.ALL, 5)

        # right
        right_box = wx.BoxSizer(wx.VERTICAL)
        right_box.Add(recieve_area_box, 1, wx.EXPAND | wx.ALL, 5)
        right_box.Add(send_area_box, 1, wx.EXPAND | wx.ALL, 5)

        # main
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        main_box.Add(left_box, 2, wx.EXPAND | wx.ALL, 5)
        main_box.Add(right_box, 3, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(main_box)
        self.panel.Layout()
        self.panel.Fit()
        #self.panel.Centre()

        #self.SetSizer(main_box)
        self.Layout()
        self.Fit()
        #self.Centre()


    #
    # Assistant functions
    #

    ###########################################################################
    # Get com ports.
    ###########################################################################
    def get_m_com_choices(self):
        m_com_choices = []
        port_list = list(comports())
        if len(port_list) > 0:
            for port in port_list:
                m_com_choices.append(port[0])
        else:
            m_com_choices = []

        return m_com_choices


    ###########################################################################
    # is_int
    ###########################################################################
    def is_int(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False


    ###########################################################################
    # is_hex
    ###########################################################################
    def is_hex(self, string):
        try:
            int(string, 16)
            return True
        except ValueError:
            return False


    ###########################################################################
    # is_one_bit_hex
    ###########################################################################
    def is_one_bit_hex(self, name, string):
        if (len(string) != 1):
            raise ValueError("Back code set error!\n" + name + " length is wrong! Need to be 1 bit.")

        if (not self.is_hex(string)):
            raise ValueError("Back code set error!\n" + name + " is not hex string!")

        if ((int(string, 16) < 0) or (int(string, 16) > 15)):
            raise ValueError("Back code set error!\n" + name + " is exced the range 0--F!")

        return True


    ###########################################################################
    # is_two_bit_hex
    ###########################################################################
    def is_two_bit_hex(self, name, string):
        if (len(string) != 2):
            raise ValueError("Back code set error!\n" + name + " length is wrong! Need to be 2 bit.")

        if (not self.is_hex(string)):
            raise ValueError("Back code set error!\n" + name + " is not hex string!")

        if ((int(string, 16) < 0) or (int(string, 16) > 255)):
            raise ValueError("Back code set error!\n" + name + " is exced the range 00--FF!")

        return True


    ###########################################################################
    # Set constant.
    ###########################################################################
    '''
    def set_constant(self):
        direction = self.m_direction_input.GetValue()
        interval = self.m_interval_input.GetValue()
        step_count = self.m_step_count_input.GetValue()
        pause_time_high = self.m_pause_time_high_input.GetValue()
        pause_time_low = self.m_pause_time_low_input.GetValue()

        if self.is_one_bit_hex("Direction", direction):
            self.converter.BACK_DIRECTION = direction

        if self.is_one_bit_hex("Interval", interval):
            self.converter.BACK_INTERVAL = interval

        if self.is_two_bit_hex("Step count", step_count):
            self.converter.BACK_STEP_COUNT = step_count

        if self.is_two_bit_hex("Pause time high", pause_time_high):
            self.converter.BACK_PAUSE_TIME_HIGH = pause_time_high

        if self.is_two_bit_hex("Pause time low", pause_time_low):
            self.converter.BACK_PAUSE_TIME_LOW = pause_time_low
    '''


    ###########################################################################
    # Parse text and convert to code.
    ###########################################################################
    def parse_convert(self, string):
        if (string == ""):
            raise Exception("Command list is empty!")

        else:
            pass

        string_list = string.splitlines()

        line_number = 1
        code_list = []
        for string in string_list:
            if ((string == "") or (string[0] == ";")):
                line_number = line_number + 1
                continue

            command = string.split()

            try:
                code = self.converter.convert(command)
            except Exception as e:
                raise Exception("Command Error in line: " + str(line_number) + "\n" + e.message)

            code_list.append(code)
            line_number = line_number + 1

        return code_list


    #
    # Event handle functions
    #
    ###########################################################################
    # Recieve area clear.
    ###########################################################################
    def on_recieve_clear_button_clicked(self, event):
        self.m_recieve_area.Clear()


    ###########################################################################
    # Check com ports.
    ###########################################################################
    def on_serial_check_button_clicked(self, event):
        self.m_serial_com_select.Set(self.get_m_com_choices())
        self.m_serial_com_select.SetSelection(0)


    ###########################################################################
    # Recieve area update
    ###########################################################################
    def on_recieve_area_update(self, data):
        #print "data[", data, "]"
        self.m_recieve_area.AppendText(data)


    ###########################################################################
    # Serial read error.
    ###########################################################################
    def on_serial_read_error(self, data):
        dia = wx.MessageDialog(None, data, "Error", wx.OK | wx.ICON_ERROR)
        dia.ShowModal()
        dia.Destroy()


    ###########################################################################
    # Serial open button clicked
    ###########################################################################
    def on_serial_open_button_clicked(self, event):
        try:
            self.serial_port.timeout = 1
            self.serial_port.xonxoff = 0
            self.serial_port.port = self.m_serial_com_select.GetValue()
            self.serial_port.parity = self.m_serial_checkbit_select.GetValue()[0]
            self.serial_port.baudrate = int(self.m_serial_bitrate_select.GetValue())
            self.serial_port.bytesize = int(self.m_serial_databit_select.GetValue())
            self.serial_port.stopbits = int(self.m_serial_stopbit_select.GetValue())
            self.serial_port.open()
        except Exception as e:
            dia = wx.MessageDialog(None, "COMM Open Fail!\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            self.serial_read_thread = serial_read_thread(self.serial_port, self)
            self.serial_read_thread.start()

            self.m_serial_open_button.Enable(False)
            self.m_serial_close_button.Enable(True)
            self.m_write_run_seq_button.Enable(True)


    ###########################################################################
    # Serial close button clicked
    ###########################################################################
    def on_serial_close_button_clicked(self, event):
        try:
            self.serial_port.close()
        except Exception as e:
            dia = wx.MessageDialog(None, "COMM close Fail!\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        try:
            self.run_thread.event_stop.set()
        except Exception as e:
            pass

        try:
            self.run_thread.event_run.set()
        except Exception as e:
            pass

        try:
            self.serial_read_thread.event_stop.set()
        except Exception as e:
            pass


        self.m_serial_open_button.Enable(True)
        self.m_serial_close_button.Enable(False)
        self.m_write_run_seq_button.Enable(False)


    ###########################################################################
    # Program exit.
    ###########################################################################
    def on_program_exit_button_clicked(self, event):
        try:
            self.serial_read_thread.event_stop.set()
            self.run_thread.event_stop.set()
        except Exception as e:
            pass

        self.Close()


    ###########################################################################
    # Write convert button clicked
    ###########################################################################
    def on_write_convert_button_clicked(self, event):
        '''
        try:
            self.set_constant()
        except ValueError as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return
        '''

        command_string = self.m_write_area.GetValue()

        try:
            code_list = self.parse_convert(command_string)
        except Exception as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        self.m_action_list.DeleteAllItems()

        action_index = 0
        for string in command_string.splitlines():
            if ((string == "") or (string[0] == ";")):
                continue
            else:
                command = string.split()

                #print "[command: ", command, "]"

                self.m_action_list.InsertStringItem(action_index, str(action_index + 1))
                self.m_action_list.SetStringItem(action_index, 1, str(" ".join(command)))
                self.m_action_list.SetStringItem(action_index, 2, str(" ".join(code_list[action_index])))
                self.m_action_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
                self.m_action_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
                self.m_action_list.SetColumnWidth(2, wx.LIST_AUTOSIZE)

                action_index =  action_index + 1


    ###########################################################################
    # Run write error.
    ###########################################################################
    def on_run_write_error(self, data):
        dia = wx.MessageDialog(None, data, "Error", wx.OK | wx.ICON_ERROR)
        dia.ShowModal()
        dia.Destroy()

        self.m_write_run_seq_button.Enable(True)
        self.m_write_stop_seq_button.Enable(False)


    ###########################################################################
    # Run seq finished.
    ###########################################################################
    def on_run_seq_finished(self, data):
        self.m_write_run_seq_button.Enable(True)
        self.m_write_stop_seq_button.Enable(False)


    ###########################################################################
    # Run seq button clicked
    ###########################################################################
    def on_write_run_seq_button_clicked(self, event):
        '''
        try:
            self.set_constant()
        except ValueError as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return
        '''

        command_string = self.m_write_area.GetValue()

        try:
            code_list = self.parse_convert(command_string)
        except Exception as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        #
        # A thread, will tell serial_read_thread I am running a seq, please watch the serial port message, if "Running finished", please let me know.
        #
        self.run_thread = run_thread(self.serial_port, self.serial_read_thread, code_list)
        self.run_thread.start()

        self.m_write_run_seq_button.Enable(False)
        self.m_write_stop_seq_button.Enable(True)


    ###########################################################################
    # Stop seq button clicked
    ###########################################################################
    def on_write_stop_seq_button_clicked(self, event):
        self.run_thread.event_stop.set()
        self.m_write_stop_seq_button.Enable(False)


    ###########################################################################
    # Command reset button clicked
    ###########################################################################
    def on_write_command_reset_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.converter.COMMAND_RESET).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Reset button clicked
    ###########################################################################
    def on_write_reset_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.converter.RESET).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return
            
        try:
            self.run_thread.event_stop.set()
        except Exception as e:
            pass
        
        self.serial_read_thread.event_run_finished.set()


    ###########################################################################
    # Run current button clicked
    ###########################################################################
    def on_write_run_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.converter.RUN).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Show RAM button clicked
    ###########################################################################
    def on_write_show_ram_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.converter.SHOW_RAM).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Show EEPROM button clicked
    ###########################################################################
    def on_write_show_eeprom_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.converter.SHOW_EEPROM).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Write EEPROM button clicked
    ###########################################################################
    def on_write_write_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.converter.WRITE).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Read button clicked
    ###########################################################################
    def on_write_read_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.converter.READ).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Input send button clicked
    ###########################################################################
    def on_send_button_clicked(self, event):
        '''
        try:
            self.set_constant()
        except ValueError as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return
        '''

        try:
            command = self.m_send_input.GetValue().split()
            code = self.converter.convert(command)
            self.serial_port.write("".join(code).decode("hex"))

            #print "[command: ", command, "]"
            #print "[code: ", code, "]"
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Input send hex button clicked
    ###########################################################################
    def on_send_hex_button_clicked(self, event):
        try:
            command = self.m_send_input.GetValue()

            self.serial_port.write(command.replace(" ", "").decode("hex"))
        except Exception as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Action send button clicked
    ###########################################################################
    def on_action_send_button_clicked(self, event):
        item_count = self.m_action_list.GetItemCount()
        action_index = self.m_action_list.GetFirstSelected()

        if (item_count == 0):
            dia = wx.MessageDialog(None, "The item list is empty!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        if (action_index == -1):
            dia = wx.MessageDialog(None, "No item is selected!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        code = self.m_action_list.GetItemText(action_index, 2).split()

        #print "[code: ", code, "]"

        try:
            self.serial_port.write("".join(code).decode("hex"))
        except Exception as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Action send next button clicked
    ###########################################################################
    def on_action_send_next_button_clicked(self, event):
        item_count = self.m_action_list.GetItemCount()
        action_index = self.m_action_list.GetFirstSelected()

        if (item_count == 0):
            dia = wx.MessageDialog(None, "The item list is empty!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        if (action_index == -1):
            dia = wx.MessageDialog(None, "No item is selected!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        if ((action_index + 1) >= item_count):
            dia = wx.MessageDialog(None, "This is the last command!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        self.m_action_list.Select(action_index + 1)
        code = self.m_action_list.GetItemText(action_index + 1, 2).split()

        #print "[code: ", code, "]"

        try:
            self.serial_port.write("".join(code).decode("hex"))
        except Exception as e:
            dia = wx.MessageDialog(None, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return
