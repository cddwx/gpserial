#!/usr/bin/env python
# coding=utf-8

import time
import datetime
import wx

from wx.lib.pubsub import pub
from serial import Serial
from serial.tools.list_ports import comports

from command import command
from run_thread import run_thread
from serial_read_thread import serial_read_thread
from progress_thread import progress_thread

class main_frame(wx.Frame):
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
        self.command = command()


        self.create_objects()
        self.connect_events()
        self.arrange_objects()


        pub.subscribe(self.on_recieve_area_update, "update")
        pub.subscribe(self.on_serial_read_error, "serial_read_error")
        pub.subscribe(self.on_run_write_error, "run_write_error")
        pub.subscribe(self.on_run_seq_started, "run_seq_started")
        pub.subscribe(self.on_run_seq_finished, "run_seq_finished")
        pub.subscribe(self.on_single_command_finished, "single_command_finished")


    ###########################################################################
    # Create objects
    ###########################################################################
    def create_objects(self):
        self.panel = wx.Panel(self)

        #
        # Recieve.
        #
        self.recieve_textarea = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.recieve_clear_button = wx.Button(self.panel, label=u"Clear")

        #
        # Send
        #

        self.action_list = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        self.action_list.InsertColumn(0, u"Id", format=wx.LIST_FORMAT_LEFT)
        self.action_list.InsertColumn(1, u"Command", format=wx.LIST_FORMAT_LEFT)
        self.action_list.InsertColumn(2, u"Hex code", format=wx.LIST_FORMAT_LEFT)
        self.action_list.InsertColumn(3, u"Time used", format=wx.LIST_FORMAT_LEFT)

        self.action_send_button = wx.Button(self.panel, label=u"Send")
        self.action_send_next_button = wx.Button(self.panel, label=u"Send next")


        #
        # Serial
        #
        self.serial_port_title = wx.StaticText(self.panel, label=u"Port: ")

        port_choice = self.get_port_choice()
        self.serial_port_choice = wx.Choice(self.panel, choices=port_choice)
        self.serial_port_choice.SetSelection(0)

        self.serial_bitrate_title = wx.StaticText(self.panel, label=u"Bitrate: ")

        bitrate_choice = [ u"2400", u"4800", u"9600", u"14400", u"19200", u"28800", u"57600" ]
        self.serial_bitrate_choice = wx.Choice(self.panel, choices=bitrate_choice)
        self.serial_bitrate_choice.SetStringSelection(u"9600")


        self.serial_databit_title = wx.StaticText(self.panel, label=u"Databit: ")

        databit_choice = [ u"5", u"6", u"7", u"8" ]
        self.serial_databit_choice = wx.Choice(self.panel, choices=databit_choice)
        self.serial_databit_choice.SetStringSelection(u"8")

        self.serial_checkbit_title = wx.StaticText(self.panel, label=u"Checkbit: ")

        checkbit_choice = [ u"None", u"Odd", u"Even", u"One", u"Zero" ]
        self.serial_checkbit_choice = wx.Choice(self.panel, choices=checkbit_choice)
        self.serial_checkbit_choice.SetStringSelection(u"None")


        self.serial_stopbit_title = wx.StaticText(self.panel, label=u"Stopbit: ")

        stopbit_choice = [ u"1", u"2" ]
        self.serial_stopbit_choice = wx.Choice(self.panel, choices=stopbit_choice)
        self.serial_stopbit_choice.SetStringSelection(u"1")

        self.serial_refresh_button = wx.Button(self.panel, label=u"Refresh port")

        self.serial_open_button = wx.Button(self.panel, label=u"Open port")
        self.serial_open_button.Enable()

        self.serial_close_button = wx.Button(self.panel, label=u"Close port")
        self.serial_close_button.Disable()

        self.program_exit_button = wx.Button(self.panel, label=u"Exit")


        #
        # Seq.
        #
        self.seq_textarea = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.seq_convert_button = wx.Button(self.panel, label=u"Convert seq")

        self.seq_run_button = wx.Button(self.panel, label=u"Run seq")
        self.seq_run_button.Disable()

        self.seq_stop_button = wx.Button(self.panel, label=u"Stop after here")
        self.seq_stop_button.Disable()

        #
        # Control
        #
        self.mcu_reset_button = wx.Button(self.panel, label=u"*** MCU RESET ***")
        self.send_reset_button = wx.Button(self.panel, label=u"Command reset")
        self.single_run_button = wx.Button(self.panel, label=u"= Run code =")
        self.show_ram_button = wx.Button(self.panel, label=u"Show RAM code")
        self.show_eeprom_button = wx.Button(self.panel, label=u"Show EEPROM code")
        self.write_eeprom_button = wx.Button(self.panel, label=u"Write to EEPROM")
        self.read_eeprom_button = wx.Button(self.panel, label=u"Load from EEPROM")

        #
        # Single send
        #
        self.single_input = wx.TextCtrl(self.panel, value=u"")
        self.single_send_button = wx.Button(self.panel, label=u"Send command")
        self.single_send_hex_button = wx.Button(self.panel, label=u"Send code")


    ############################################################################
    # Connect Events
    ############################################################################
    def connect_events(self):
        self.recieve_clear_button.Bind(wx.EVT_BUTTON, self.on_recieve_clear_button_clicked)

        self.serial_refresh_button.Bind(wx.EVT_BUTTON, self.on_serial_refresh_button_clicked)
        self.serial_open_button.Bind(wx.EVT_BUTTON, self.on_serial_open_button_clicked)
        self.serial_close_button.Bind(wx.EVT_BUTTON, self.on_serial_close_button_clicked)
        self.program_exit_button.Bind(wx.EVT_BUTTON, self.on_program_exit_button_clicked)

        self.action_send_button.Bind(wx.EVT_BUTTON, self.on_action_send_button_clicked)
        self.action_send_next_button.Bind(wx.EVT_BUTTON, self.on_action_send_next_button_clicked)

        self.seq_convert_button.Bind(wx.EVT_BUTTON, self.on_seq_convert_button_clicked)
        self.seq_run_button.Bind(wx.EVT_BUTTON, self.on_seq_run_button_clicked)
        self.seq_stop_button.Bind(wx.EVT_BUTTON, self.on_seq_stop_button_clicked)

        self.single_send_button.Bind(wx.EVT_BUTTON, self.on_single_send_button_clicked)
        self.single_send_hex_button.Bind(wx.EVT_BUTTON, self.on_single_send_hex_button_clicked)

        self.mcu_reset_button.Bind(wx.EVT_BUTTON, self.on_mcu_reset_button_clicked)
        self.send_reset_button.Bind(wx.EVT_BUTTON, self.on_send_reset_button_clicked)
        self.single_run_button.Bind(wx.EVT_BUTTON, self.on_single_run_button_clicked)
        self.show_ram_button.Bind(wx.EVT_BUTTON, self.on_show_ram_button_clicked)
        self.show_eeprom_button.Bind(wx.EVT_BUTTON, self.on_show_eeprom_button_clicked)
        self.write_eeprom_button.Bind(wx.EVT_BUTTON, self.on_write_eeprom_button_clicked)
        self.read_eeprom_button.Bind(wx.EVT_BUTTON, self.on_read_eeprom_button_clicked)


    ############################################################################
    # Arrange objects.
    # I find it is more confortable to arrange from big to small.
    ############################################################################
    def arrange_objects(self):
        #
        ##### Serial port box
        #
        serial_port_box = wx.BoxSizer(wx.HORIZONTAL)
        serial_port_box.Add(self.serial_port_title, 1, wx.ALIGN_CENTER_VERTICAL)
        serial_port_box.Add(self.serial_port_choice, 1, wx.ALIGN_CENTER_VERTICAL)

        #
        ##### Serial bitrate box
        #
        serial_bitrate_box = wx.BoxSizer(wx.HORIZONTAL)
        serial_bitrate_box.Add(self.serial_bitrate_title, 1, wx.ALIGN_CENTER_VERTICAL)
        serial_bitrate_box.Add(self.serial_bitrate_choice, 1, wx.ALIGN_CENTER_VERTICAL)

        #
        ##### Serial databit box
        #
        serial_databit_box = wx.BoxSizer(wx.HORIZONTAL)
        serial_databit_box.Add(self.serial_databit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        serial_databit_box.Add(self.serial_databit_choice, 1, wx.ALIGN_CENTER_VERTICAL)

        #
        ##### Serial checkbit box
        #
        serial_checkbit_box = wx.BoxSizer(wx.HORIZONTAL)
        serial_checkbit_box.Add(self.serial_checkbit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        serial_checkbit_box.Add(self.serial_checkbit_choice, 1, wx.ALIGN_CENTER_VERTICAL)

        #
        ##### Serial stopbit box
        #
        serial_stopbit_box = wx.BoxSizer(wx.HORIZONTAL)
        serial_stopbit_box.Add(self.serial_stopbit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        serial_stopbit_box.Add(self.serial_stopbit_choice, 1, wx.ALIGN_CENTER_VERTICAL)

        #
        #### Parameter box
        #
        parameter_box = wx.BoxSizer(wx.VERTICAL)
        parameter_box.Add(serial_port_box, 1, wx.EXPAND)
        parameter_box.Add(serial_bitrate_box, 1, wx.EXPAND)
        parameter_box.Add(serial_databit_box, 1, wx.EXPAND)
        parameter_box.Add(serial_checkbit_box, 1, wx.EXPAND)
        parameter_box.Add(serial_stopbit_box, 1, wx.EXPAND)


        #
        ##### Serial refresh button box
        #
        serial_refresh_button_box = wx.BoxSizer(wx.HORIZONTAL)
        serial_refresh_button_box.Add(self.serial_refresh_button, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        
        #
        ##### Serial open button box
        #
        serial_open_button_box = wx.BoxSizer(wx.HORIZONTAL)
        serial_open_button_box.Add(self.serial_open_button, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        
        #
        ##### Serial close button box
        #
        serial_close_button_box = wx.BoxSizer(wx.HORIZONTAL)
        serial_close_button_box.Add(self.serial_close_button, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        
        #
        #
        ##### Program exit button box
        #
        program_exit_button_box = wx.BoxSizer(wx.HORIZONTAL)
        program_exit_button_box.Add(self.program_exit_button, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        
        #
        #### Operate box
        #
        operate_box = wx.BoxSizer(wx.VERTICAL)
        operate_box.Add(serial_refresh_button_box, 1, wx.EXPAND)
        operate_box.Add(serial_open_button_box, 1, wx.EXPAND)
        operate_box.Add(serial_close_button_box, 1, wx.EXPAND)
        operate_box.Add(program_exit_button_box, 1, wx.EXPAND)

        #
        ### Setting box
        #
        setting_box = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel, u"Setting area")
        setting_box.Add(parameter_box, 2, wx.EXPAND | wx.ALL, 5)
        setting_box.Add(operate_box, 1, wx.EXPAND | wx.ALL, 5)

        #
        #### Seq textarea box
        #
        seq_textarea_box = wx.BoxSizer(wx.HORIZONTAL)
        seq_textarea_box.Add(self.seq_textarea, 1, wx.EXPAND | wx.ALL, 5)

        #
        #### Seq send buttons box
        #
        seq_send_buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        seq_send_buttons_box.Add(self.seq_convert_button, 1, wx.ALL, 5)
        seq_send_buttons_box.Add(self.seq_run_button, 1, wx.ALL, 5)
        seq_send_buttons_box.Add(self.seq_stop_button, 1, wx.ALL, 5)

        #
        ### Seq send box
        #
        seq_send_box = wx.StaticBoxSizer(wx.VERTICAL, self.panel, u"Seq send area")
        seq_send_box.Add(seq_textarea_box, 1, wx.EXPAND)
        seq_send_box.Add(seq_send_buttons_box, 0, wx.EXPAND)

        #
        #### Single send buttons box
        #
        single_input_box = wx.BoxSizer(wx.HORIZONTAL)
        single_input_box.Add(self.single_input, 1, wx.ALL, 5)

        #
        #### Single send buttons box
        #
        single_send_buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        single_send_buttons_box.Add(self.single_send_button, 1, wx.ALL, 5)
        single_send_buttons_box.Add(self.single_send_hex_button, 1, wx.ALL, 5)

        #
        ### Single send box
        #
        single_send_box = wx.StaticBoxSizer(wx.VERTICAL, self.panel, u"Single send area")
        single_send_box.Add(single_input_box, 0, wx.EXPAND)
        single_send_box.Add(single_send_buttons_box, 0, wx.EXPAND)

        #
        ##### Control buttons1 box
        #
        control_buttons1_box = wx.BoxSizer(wx.HORIZONTAL)
        control_buttons1_box.Add(self.mcu_reset_button, 1, wx.ALL, 5)

        #
        ##### Control buttons2 box
        #
        control_buttons2_box = wx.BoxSizer(wx.HORIZONTAL)
        control_buttons2_box.Add(self.send_reset_button, 1, wx.ALL, 5)
        control_buttons2_box.Add(self.single_run_button, 1, wx.ALL, 5)

        #
        ##### Control buttons3 box
        #
        control_buttons3_box = wx.BoxSizer(wx.HORIZONTAL)
        control_buttons3_box.Add(self.show_ram_button, 1, wx.ALL, 5)
        control_buttons3_box.Add(self.show_eeprom_button, 1, wx.ALL, 5)

        #
        ##### Control buttons4 box
        #
        control_buttons4_box = wx.BoxSizer(wx.HORIZONTAL)
        control_buttons4_box.Add(self.write_eeprom_button, 1, wx.ALL, 5)
        control_buttons4_box.Add(self.read_eeprom_button, 1, wx.ALL, 5)

        #
        ### Control box
        #
        control_box = wx.StaticBoxSizer(wx.VERTICAL, self.panel, u"Control area")
        control_box.Add(control_buttons1_box, 0, wx.EXPAND)
        control_box.Add(control_buttons2_box, 0, wx.EXPAND)
        control_box.Add(control_buttons3_box, 0, wx.EXPAND)
        control_box.Add(control_buttons4_box, 0, wx.EXPAND)


        #
        ### Recieve box
        #
        recieve_box = wx.StaticBoxSizer(wx.VERTICAL, self.panel, u"Recieve area")
        recieve_box.Add(self.recieve_textarea, 1, wx.EXPAND | wx.ALL, 5)
        recieve_box.Add(self.recieve_clear_button, 0, wx.ALL, 5)

        #
        #### Action list box
        #
        action_list_box = wx.BoxSizer(wx.HORIZONTAL)
        action_list_box.Add(self.action_list, 1, wx.EXPAND | wx.ALL, 5)

        #
        #### Action send buttons box
        #
        action_send_buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        action_send_buttons_box.Add(self.action_send_button, 1, wx.ALL, 5)
        action_send_buttons_box.Add(self.action_send_next_button, 1, wx.ALL, 5)

        #
        ### Action send box
        #
        action_send_box = wx.StaticBoxSizer(wx.VERTICAL, self.panel, u"List send area")
        action_send_box.Add(action_list_box, 1, wx.EXPAND)
        action_send_box.Add(action_send_buttons_box, 0, wx.EXPAND)


        #
        ## Left
        #
        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(setting_box, 0, wx.EXPAND | wx.ALL, 5)
        left_box.Add(seq_send_box, 2, wx.EXPAND | wx.ALL, 5)
        left_box.Add(single_send_box, 1, wx.EXPAND | wx.ALL, 5)
        left_box.Add(control_box, 0, wx.EXPAND | wx.ALL, 5)

        #
        ## Right
        #
        right_box = wx.BoxSizer(wx.VERTICAL)
        right_box.Add(recieve_box, 1, wx.EXPAND | wx.ALL, 5)
        right_box.Add(action_send_box, 1, wx.EXPAND | wx.ALL, 5)

        #
        # Main box
        #
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        main_box.Add(left_box, 1, wx.EXPAND)
        main_box.Add(right_box, 2, wx.EXPAND)

        self.panel.SetSizer(main_box)
        self.panel.Fit()

        self.Fit()


    #
    # Assistant functions
    #

    ###########################################################################
    # Get com ports.
    ###########################################################################
    def get_port_choice(self):
        port_choice = []
        port_list = list(comports())
        if len(port_list) > 0:
            for port in port_list:
                port_choice.append(port[0])
        else:
            port_choice = []

        return port_choice


    #
    # Event handle functions
    #
    ###########################################################################
    # Recieve area clear.
    ###########################################################################
    def on_recieve_clear_button_clicked(self, event):
        self.recieve_textarea.Clear()


    ###########################################################################
    # Check com ports.
    ###########################################################################
    def on_serial_refresh_button_clicked(self, event):
        self.serial_port_choice.Set(self.get_port_choice())
        self.serial_port_choice.SetSelection(0)


    ###########################################################################
    # Recieve area update
    ###########################################################################
    def on_recieve_area_update(self, data):
        #print "data[", data, "]"
        self.recieve_textarea.AppendText(data)


    ###########################################################################
    # Serial read error.
    ###########################################################################
    def on_serial_read_error(self, data):
        dia = wx.MessageDialog(self, data, "Error", wx.OK | wx.ICON_ERROR)
        dia.ShowModal()
        dia.Destroy()


    ###########################################################################
    # Serial open button clicked
    ###########################################################################
    def on_serial_open_button_clicked(self, event):
        try:
            self.serial_port.timeout = 1
            self.serial_port.xonxoff = 0
            self.serial_port.port = str(self.serial_port_choice.GetString(self.serial_port_choice.GetSelection()))
            self.serial_port.baudrate = int(self.serial_bitrate_choice.GetString(self.serial_bitrate_choice.GetSelection()))
            self.serial_port.parity = self.serial_checkbit_choice.GetString(self.serial_checkbit_choice.GetSelection())[0]
            self.serial_port.bytesize = int(self.serial_databit_choice.GetString(self.serial_databit_choice.GetSelection()))
            self.serial_port.stopbits = int(self.serial_stopbit_choice.GetString(self.serial_stopbit_choice.GetSelection()))
            self.serial_port.open()
        except Exception as e:
            dia = wx.MessageDialog(self, "COMM Open Fail!\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        try:
            self.serial_port.write("".join(self.command.COMMAND_RESET).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        self.serial_read_thread = serial_read_thread(self.serial_port, self)
        self.serial_read_thread.start()

        self.serial_open_button.Disable()
        self.serial_close_button.Enable()
        self.seq_run_button.Enable()


    ###########################################################################
    # Serial close button clicked
    ###########################################################################
    def on_serial_close_button_clicked(self, event):
        try:
            self.serial_port.close()
        except Exception as e:
            dia = wx.MessageDialog(self, "COMM close Fail!\n" + e.message, "Error", wx.OK | wx.ICON_ERROR)
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


        self.serial_open_button.Enable()
        self.serial_close_button.Disable()
        self.seq_run_button.Disable()


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
    # Seq convert button clicked
    ###########################################################################
    def on_seq_convert_button_clicked(self, event):
        command_string = self.seq_textarea.GetValue()

        try:
            code_list = self.command.parse_convert(command_string)
        except Exception as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        self.action_list.DeleteAllItems()

        action_index = 0
        for code in code_list:
            command_time = datetime.timedelta(milliseconds=int(code[2]))
            command_time_string = str(command_time.seconds / 3600) + "h " + str(command_time.seconds % 3600 / 60) + "m " + str(command_time.seconds % 3600 % 60) + "s"

            self.action_list.InsertItem(action_index, str(action_index + 1))
            self.action_list.SetItem(action_index, 1, str(" ".join(code[0])))
            self.action_list.SetItem(action_index, 2, str(" ".join(code[1])))
            self.action_list.SetItem(action_index, 3, command_time_string)
            self.action_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.action_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.action_list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
            self.action_list.SetColumnWidth(3, wx.LIST_AUTOSIZE)

            action_index =  action_index + 1

        total_time = datetime.timedelta(milliseconds=int(code_list[-1][3]))
        total_time_string = str(total_time.seconds / 3600) + " hours " + str(total_time.seconds % 3600 / 60) + " minutes " + str(total_time.seconds % 3600 % 60) + " seconds"
        dia = wx.MessageDialog(self,  "Total time: " + total_time_string, "Total time", wx.OK | wx.ICON_INFORMATION)
        dia.ShowModal()
        dia.Destroy()


    ###########################################################################
    # Run write error.
    ###########################################################################
    def on_run_write_error(self, data):
        dia = wx.MessageDialog(self, data, "Error", wx.OK | wx.ICON_ERROR)
        dia.ShowModal()
        dia.Destroy()

        self.seq_run_button.Enable()
        self.seq_stop_button.Disable()


    ###########################################################################
    # Run seq started.
    ###########################################################################
    def on_run_seq_started(self, data):
        self.serial_close_button.Disable()

        self.seq_convert_button.Disable()
        self.seq_run_button.Disable()
        self.seq_stop_button.Enable()

        self.send_reset_button.Disable()
        self.single_run_button.Disable()
        self.show_ram_button.Disable()
        self.show_eeprom_button.Disable()
        self.write_eeprom_button.Disable()
        self.read_eeprom_button.Disable()

        self.single_send_button.Disable()
        self.single_send_hex_button.Disable()

        self.action_list.Disable()
        self.action_send_button.Disable()
        self.action_send_next_button.Disable()



    ###########################################################################
    # Single command finished.
    ###########################################################################
    def on_single_command_finished(self, data):
        code_list = data[0]
        count = data[1]

        if ((count + 1) < len(code_list)):
            self.action_list.Select(count + 1)
            self.action_list.Focus(count + 1)

            """
            command_time = datetime.timedelta(milliseconds=int(code_list[count + 1][2]))
            command_time_string = str(command_time.seconds / 3600) + " hours " + str(command_time.seconds % 3600 / 60) + " minutes " + str(command_time.seconds % 3600 % 60) + " seconds"

            message = '''\
Current command             : %s
Current command last time   : %s''' %(" ".join(code_list[count + 1][0]), command_time_string)
            """
        else:
            """
            message = "End."
            """
            pass

        """
        self.progress_dia.Update(int(code_list[count][3]), newmsg=message)
        self.progress_dia.Fit()
        """


    ###########################################################################
    # Run seq finished.
    ###########################################################################
    def on_run_seq_finished(self, data):
        dia = wx.MessageDialog(self, "Run seq finished!", "Finished", wx.OK | wx.ICON_INFORMATION)
        dia.ShowModal()
        dia.Destroy()

        self.serial_close_button.Enable()

        self.seq_convert_button.Enable()
        self.seq_run_button.Enable()
        self.seq_stop_button.Disable()

        self.send_reset_button.Enable()
        self.single_run_button.Enable()
        self.show_ram_button.Enable()
        self.show_eeprom_button.Enable()
        self.write_eeprom_button.Enable()
        self.read_eeprom_button.Enable()

        self.single_send_button.Enable()
        self.single_send_hex_button.Enable()

        self.action_send_button.Enable()
        self.action_send_next_button.Enable()


    ###########################################################################
    # Run seq button clicked
    ###########################################################################
    def on_seq_run_button_clicked(self, event):
        command_string = self.seq_textarea.GetValue()

        try:
            code_list = self.command.parse_convert(command_string)
        except Exception as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        self.action_list.DeleteAllItems()

        action_index = 0
        for code in code_list:
            command_time = datetime.timedelta(milliseconds=int(code[2]))
            command_time_string = str(command_time.seconds / 3600) + "h " + str(command_time.seconds % 3600 / 60) + "m " + str(command_time.seconds % 3600 % 60) + "s"

            self.action_list.InsertItem(action_index, str(action_index + 1))
            self.action_list.SetItem(action_index, 1, str(" ".join(code[0])))
            self.action_list.SetItem(action_index, 2, str(" ".join(code[1])))
            self.action_list.SetItem(action_index, 3, command_time_string)
            self.action_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.action_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.action_list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
            self.action_list.SetColumnWidth(3, wx.LIST_AUTOSIZE)

            action_index =  action_index + 1

        self.action_list.Select(0)

        """
        command_time = datetime.timedelta(milliseconds=int(code_list[0][2]))
        command_time_string = str(command_time.seconds / 3600) + " hours " + str(command_time.seconds % 3600 / 60) + " minutes " + str(command_time.seconds % 3600 % 60) + " seconds"

        message = '''\
Current command             : %s
Current command last time   : %s''' %(" ".join(code_list[0][0]), command_time_string)

        self.progress_dia = wx.ProgressDialog("Running", message , int(code_list[-1][3]), self, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_ESTIMATED_TIME)
        """

        #
        # A thread, will tell serial_read_thread I am running a seq, please watch the serial port message, if "Running finished", please let me know.
        #
        self.run_thread = run_thread(self.serial_port, self.serial_read_thread, code_list)
        self.run_thread.start()


    ###########################################################################
    # Stop seq button clicked
    ###########################################################################
    def on_seq_stop_button_clicked(self, event):
        self.run_thread.event_stop.set()
        self.seq_stop_button.Disable()


    ###########################################################################
    # Command reset button clicked
    ###########################################################################
    def on_send_reset_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.command.COMMAND_RESET).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Reset button clicked
    ###########################################################################
    def on_mcu_reset_button_clicked(self, event):
        try:
            run_seq = self.serial_read_thread.event_run_seq.is_set()
        except Exception as e:
            serial_read_thread_alive = False
        else:
            serial_read_thread_alive = True

        if (serial_read_thread_alive == True):
            #
            # When running seq.
            #
            if (self.serial_read_thread.event_run_seq.is_set() == True):
                self.run_thread.event_stop.set()
                self.serial_read_thread.event_run_finished.set()
            #
            # When NOT running seq.
            #
            else:
                pass

            try:
                self.serial_port.write("".join(self.command.RESET).decode("hex"))
            except (ValueError, Exception) as e:
                dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
                dia.ShowModal()
                dia.Destroy()

                return
        else:
            dia = wx.MessageDialog(self, "Serial port not open.", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return



    ###########################################################################
    # Run current button clicked
    ###########################################################################
    def on_single_run_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.command.RUN).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Show RAM button clicked
    ###########################################################################
    def on_show_ram_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.command.SHOW_RAM).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Show EEPROM button clicked
    ###########################################################################
    def on_show_eeprom_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.command.SHOW_EEPROM).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Write EEPROM button clicked
    ###########################################################################
    def on_write_eeprom_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.command.WRITE).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Read eeprom button clicked
    ###########################################################################
    def on_read_eeprom_button_clicked(self, event):
        try:
            self.serial_port.write("".join(self.command.READ).decode("hex"))
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Single send button clicked
    ###########################################################################
    def on_single_send_button_clicked(self, event):
        '''
        try:
            self.set_constant()
        except ValueError as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return
        '''

        try:
            command = self.single_input.GetValue().split()
            code = self.command.convert(command)
            self.serial_port.write("".join(code).decode("hex"))

            #print "[command: ", command, "]"
            #print "[code: ", code, "]"
        except (ValueError, Exception) as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Single send hex button clicked
    ###########################################################################
    def on_single_send_hex_button_clicked(self, event):
        try:
            command = self.single_input.GetValue()
            print "[command: ", command, "]"

            self.serial_port.write(command.replace(" ", "").decode("hex"))
        except Exception as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Action send button clicked
    ###########################################################################
    def on_action_send_button_clicked(self, event):
        item_count = self.action_list.GetItemCount()
        action_index = self.action_list.GetFirstSelected()

        if (item_count == 0):
            dia = wx.MessageDialog(self, "The item list is empty!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        if (action_index == -1):
            dia = wx.MessageDialog(self, "No item is selected!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        code = self.action_list.GetItemText(action_index, 2).split()

        #print "[code: ", code, "]"

        try:
            self.serial_port.write("".join(code).decode("hex"))
        except Exception as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return


    ###########################################################################
    # Action send next button clicked
    ###########################################################################
    def on_action_send_next_button_clicked(self, event):
        item_count = self.action_list.GetItemCount()
        action_index = self.action_list.GetFirstSelected()

        if (item_count == 0):
            dia = wx.MessageDialog(self, "The item list is empty!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        if (action_index == -1):
            dia = wx.MessageDialog(self, "No item is selected!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        if ((action_index + 1) >= item_count):
            dia = wx.MessageDialog(self, "This is the last command!", "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return

        else:
            pass

        self.action_list.Select(action_index + 1)
        self.action_list.Focus(action_index + 1)
        code = self.action_list.GetItemText(action_index + 1, 2).split()

        #print "[code: ", code, "]"

        try:
            self.serial_port.write("".join(code).decode("hex"))
        except Exception as e:
            dia = wx.MessageDialog(self, e.message, "Error", wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()

            return
