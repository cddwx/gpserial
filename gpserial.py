#!/usr/bin/env python
# coding=utf-8

import os
import io
import time
import threading
import json

import wx
from wx.lib import buttons

from wx.lib.pubsub import pub

import serial.tools.list_ports
from serial import Serial


class move_parameter_dialog(wx.Dialog):
    def __init__(self, functions):
        wx.Dialog.__init__(
                self,
                parent=None,
                id=wx.ID_ANY,
                title=u"运动参数设置",
                pos=wx.DefaultPosition,
                size=wx.DefaultSize
        )

        self.functions = functions

        self.panel = wx.Panel(self)

        # Function selection area.
        self.function_area_title = wx.StaticText(self.panel, label=u"选择运动函数", style=wx.ALIGN_BOTTOM)

        function_verbose_names = []
        for element in self.functions:
            function_verbose_names.append(element['verbose_name'])

        self.function_area_function_list_box = wx.ListBox(self.panel, choices=function_verbose_names, style=wx.LB_SINGLE)
        self.function_area_function_list_box.SetSelection(0)

        # Parameter setting area.
        self.function_description_title = wx.StaticText(self.panel, label=u"函数描述")

        self.parameter_setting_title = wx.StaticText(self.panel, label=u"函数参数设置")

        # Operation area.
        self.ok_button = wx.Button(self.panel, wx.ID_OK, u"确认添加")
        self.cancel_button = wx.Button(self.panel, wx.ID_CANCEL, u"取消")


        # Arrangement.
        box_function_list = wx.FlexGridSizer(0, 1)
        box_function_list.Add(self.function_area_title, 0, wx.ALIGN_BOTTOM)
        box_function_list.Add(self.function_area_function_list_box, 0, wx.EXPAND)
        box_function_list.AddGrowableRow(1, 1)
        box_function_list.AddGrowableCol(0, 1)


        self.right_hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.right_hbox2.Add(wx.TextCtrl(self.panel, value=self.functions[0]['description'], style=wx.TE_MULTILINE | wx.TE_READONLY), 1, wx.EXPAND)

        self.title_button = []
        self.value_input = []
        parameter_hbox = []
        for one_dict in self.functions[0]['parameter']:
            self.title_button.append(wx.StaticText(self.panel, label=one_dict['verbose_name']))
            self.value_input.append(wx.TextCtrl(self.panel, value=one_dict['value']))

            parameter_hbox.append(wx.BoxSizer(wx.HORIZONTAL))
            parameter_hbox[-1].Add(self.title_button[-1], 1, wx.ALIGN_CENTER_VERTICAL)
            parameter_hbox[-1].Add(self.value_input[-1], 1, wx.ALIGN_CENTER_VERTICAL)

        parameter_vbox = wx.BoxSizer(wx.VERTICAL)
        for one_element in parameter_hbox:
            parameter_vbox.Add(one_element, 0, wx.EXPAND)

        self.right_hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.right_hbox4.Add(parameter_vbox, 1, wx.EXPAND)

        box_function_parameter = wx.GridBagSizer()
        box_function_parameter.Add(self.function_description_title, (0, 0), (1, 2), wx.ALIGN_BOTTOM)
        box_function_parameter.Add(self.right_hbox2, (1, 0), (1, 2), wx.EXPAND)
        box_function_parameter.Add(self.parameter_setting_title, (2, 0), (1, 2), wx.ALIGN_BOTTOM)
        box_function_parameter.Add(self.right_hbox4, (3, 0), (1, 2), wx.EXPAND)
        box_function_parameter.Add(self.ok_button, (4,0), (1, 1), wx.ALIGN_CENTER_HORIZONTAL)
        box_function_parameter.Add(self.cancel_button, (4,1), (1, 1), wx.ALIGN_CENTER_HORIZONTAL)
        box_function_parameter.AddGrowableCol(0, 1)


        main_box = wx.BoxSizer(wx.HORIZONTAL)
        main_box.Add(box_function_list, 1, wx.EXPAND | wx.ALL, 5)
        main_box.Add(box_function_parameter, 2, wx.EXPAND | wx.ALL, 5)


        self.panel.SetSizer(main_box)
        self.panel.Layout()
        self.panel.Fit()

        self.Layout()
        self.Fit()

        # Connect Events
        self.function_area_function_list_box.Bind(wx.EVT_LISTBOX, self.on_function_area_function_list_box_selected)


    # Event handlers
    def on_function_area_function_list_box_selected(self, event):
        function = self.functions[self.function_area_function_list_box.GetSelection()]

        self.right_hbox2.Clear(True)
        self.right_hbox4.Clear(True)

        function_description = wx.TextCtrl(self.panel, value=function['description'], style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.right_hbox2.Add(function_description, 1, wx.EXPAND)


        parameter_vbox = wx.BoxSizer(wx.VERTICAL)
        
        box = []
        self.title_button = []
        self.value_input = []
        for one_dict in function['parameter']:
            self.title_button.append(wx.StaticText(self.panel, label=one_dict['verbose_name']))
            self.value_input.append(wx.TextCtrl(self.panel, value=one_dict['value']))

            box.append(wx.BoxSizer(wx.HORIZONTAL))
            box[-1].Add(self.title_button[-1], 1, wx.ALIGN_CENTER_VERTICAL)
            box[-1].Add(self.value_input[-1], 1, wx.ALIGN_CENTER_VERTICAL)

            parameter_vbox.Add(box[-1], 0, wx.EXPAND)

        self.right_hbox4.Add(parameter_vbox, 1, wx.EXPAND)

        self.panel.Layout()
        self.panel.Fit()

        self.Layout()
        self.Fit()

    #def on_ok_button_clicked(self, event):

    #def on_cancel_button_clicked(self, event):


class serial_frame(wx.Frame):
    MIN_PERIOD = '0102'
    MIN_SPEED = ''
    MAX_SPEED = ''
    DEFAULT_SPEED = '5'
    MIN_DISTANCE = '00'

    actions = []
    functions = [
        {
            'function_name' : 'move_distance',
            'verbose_name'  : u'按长度移动',
            'description'   : u'向某一方向以某一速度移动某一距离',
            'parameter'     : [
                {
                    'name'          : 'direct',
                    'verbose_name'  : u'方向',
                    'value'         : '',
                },
                {
                    'name'          : 'speed',
                    'verbose_name'  : u'速度',
                    'value'         : '',
                },
                {
                    'name'          : 'distance',
                    'verbose_name'  : u'距离',
                    'value'         : '',
                },

            ],
        },
        {
            'function_name' : 'classical_move',
            'verbose_name'  : u'经典条带沉积移动',
            'description'   : u'将以下动作循环执行某一次数---向某一方向以某一速度移动某一距离然后暂停某一时间',
            'parameter'     : [
                {
                    'name'          : 'direct',
                    'verbose_name'  : u'方向',
                    'value'         : '',
                },
                {
                    'name'          : 'speed',
                    'verbose_name'  : u'速度',
                    'value'         : '',
                },
                {
                    'name'          : 'step_distance',
                    'verbose_name'  : u'距离',
                    'value'         : '',
                },
                {
                    'name'          : 'pause_time',
                    'verbose_name'  : u'停留时间',
                    'value'         : '',
                },
                {
                    'name'          : 'count',
                    'verbose_name'  : u'循环次数',
                    'value'         : '',
                },
            ],
        },
        {
            'function_name' : 'pause',
            'verbose_name'  : u'暂停',
            'description'   : u'暂停某一段时间',
            'parameter'     : [
                {
                    'name'          : 'time',
                    'verbose_name'  : u'时间',
                    'value'         : '',
                },
            ],
        },
    ]


    def __init__(self, serial_obj):
        wx.Frame.__init__(
                self,
                parent=None,
                id=wx.ID_ANY,
                title=u"OUYANG Lab 提拉机指令发送程序 V1.0",
                pos=wx.DefaultPosition,
                size=wx.DefaultSize,
        )

        self.ser = serial_obj

        #self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        #self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        #self.SetBackgroundColour(wx.SystemSettings.GetColour(addwx.SYS_COLOUR_WINDOWFRAME))

        panel = wx.Panel(self)

        # Recieve objects.
        self.m_recieve_title = wx.StaticText(panel, label=u"接收区")
        self.m_recieve_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.m_hex_show_checkbox = wx.CheckBox(panel, label=u"HEX显示")
        self.m_recieve_clear_button = wx.Button(panel, label=u"清空")

        # Send objects.
        self.m_send_title = wx.StaticText(panel, label=u"发送区")
        self.m_send_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.m_hex_send_checkbox = wx.CheckBox(panel, label=u"HEX发送")
        self.m_send_clear_button = wx.Button(panel, wx.ID_ANY, u"清空")
        self.m_send_input = wx.TextCtrl(panel)
        self.m_send_button = wx.Button(panel, label=u"发送")

        # Serial parameter setting.
        self.m_serial_title = wx.StaticText(panel, label=u"串口设置")

        self.m_serial_com_title = wx.StaticText(panel, label=u"通讯端口：")

        #m_com_choices = [ u"COM1", u"COM2", u"COM3", u"COM4", u"COM5", u"COM6", u"COM7", u"COM8", u"COM9" ]
        m_com_choices = []
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) > 0:
            for port in port_list:
                m_com_choices.append(port[0])
        else:
            m_com_choices = []

        self.m_serial_com_select = wx.ComboBox(panel, choices=m_com_choices, style=wx.CB_READONLY)
        self.m_serial_com_select.SetSelection(0)


        self.m_serial_bitrate_title = wx.StaticText(panel, label=u"波特率：")

        m_bitrate_choices = [ u"2400", u"4800", u"9600", u"14400", u"19200", u"28800", u"57600" ]
        self.m_serial_bitrate_select = wx.ComboBox(panel, choices=m_bitrate_choices, style=wx.CB_READONLY)
        self.m_serial_bitrate_select.SetSelection(2)


        self.m_serial_databit_title = wx.StaticText(panel, label=u"数据位：")

        m_databit_choices = [ u"5", u"6", u"7", u"8" ]
        self.m_serial_databit_select = wx.ComboBox(panel, choices=m_databit_choices, style=wx.CB_READONLY)
        self.m_serial_databit_select.SetSelection(3)

        self.m_serial_checkbit_title = wx.StaticText(panel, label=u"校验位：")

        m_checkbit_choices = [ u"None", u"Odd", u"Even", u"One", u"Zero" ]
        self.m_serial_checkbit_select = wx.ComboBox(panel, choices=m_checkbit_choices, style=wx.CB_READONLY)
        self.m_serial_checkbit_select.SetSelection(0)


        self.m_serial_stopbit_title = wx.StaticText(panel, label=u"停止位：")

        m_stopbit_choices = [ u"1", u"2" ]
        self.m_serial_stopbit_select = wx.ComboBox(panel, choices=m_stopbit_choices, style=wx.CB_READONLY)
        self.m_serial_stopbit_select.SetSelection(0)

        self.m_serial_open_button = buttons.GenButton(panel, wx.ID_ANY, u"打开串口")
        self.m_serial_open_button.Enable(True)

        self.m_serial_close_button = buttons.GenButton(panel, wx.ID_ANY, u"关闭串口")
        self.m_serial_close_button.Enable(False)


        # Move parameter.
        self.m_action_title = wx.StaticText(panel, label=u"运动参数设置")

        self.m_action_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_HRULES)
        self.m_action_list.InsertColumn(0, u"序号", format=wx.LIST_FORMAT_LEFT)
        self.m_action_list.InsertColumn(1, u"运动类型", format=wx.LIST_FORMAT_LEFT)
        self.m_action_list.InsertColumn(2, u"运动参数", format=wx.LIST_FORMAT_LEFT)

        self.m_action_motor_step_select_title = wx.StaticText(panel, label=u"电机步长：")

        m_motor_step_choices = [ u"2.4", u"1.557" ]
        self.m_action_motor_step_select = wx.ComboBox(panel, choices=m_motor_step_choices, style=wx.CB_READONLY)
        self.m_action_motor_step_select.SetSelection(0)

        self.m_action_up_button = wx.Button(panel, label=u"上移")
        self.m_action_down_button = wx.Button(panel, label=u"下移")
        self.m_action_delete_button = wx.Button(panel, label=u"删除")
        self.m_action_edit_button = wx.Button(panel, label=u"编辑")

        self.m_action_add_button = wx.Button(panel, label=u"添加运动")
        self.m_action_save_button = wx.Button(panel, label=u"保存运动")
        self.m_action_load_button = wx.Button(panel, label=u"载入运动")
        self.m_action_send_button = wx.Button(panel, label=u"发送HEX指令")

        # Program operation.
        self.m_program_exit_button = wx.Button(panel, label=u"退出程序")


        # Arrangement.
        box_recieve = wx.GridBagSizer()
        box_recieve.Add(self.m_recieve_title,           (0, 0), (1, 2), wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        box_recieve.Add(self.m_recieve_area,            (1, 0), (1, 2), wx.EXPAND)
        box_recieve.Add(self.m_hex_show_checkbox,       (2, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        box_recieve.Add(self.m_recieve_clear_button,    (2, 1), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        box_recieve.AddGrowableRow(1, 1)
        box_recieve.AddGrowableCol(0, 1)
        box_recieve.AddGrowableCol(1, 1)


        box_send = wx.GridBagSizer()
        box_send.Add(self.m_send_title,         (0, 0), (1, 6), wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        box_send.Add(self.m_send_area,          (1, 0), (1, 6), wx.EXPAND)
        box_send.Add(self.m_hex_send_checkbox,  (2, 0), (1, 3), wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        box_send.Add(self.m_send_clear_button,  (2, 3), (1, 3), wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        box_send.Add(self.m_send_input,         (3, 0), (1, 5), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_send.Add(self.m_send_button,        (3, 5), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        box_send.AddGrowableRow(1, 1)
        box_send.AddGrowableCol(0, 1)
        box_send.AddGrowableCol(1, 1)
        box_send.AddGrowableCol(2, 1)
        box_send.AddGrowableCol(3, 1)
        box_send.AddGrowableCol(4, 1)
        box_send.AddGrowableCol(5, 1)

        box_serial_parameter_com = wx.BoxSizer(wx.HORIZONTAL)
        box_serial_parameter_com.Add(self.m_serial_com_title, 1, wx.ALIGN_CENTER_VERTICAL)
        box_serial_parameter_com.Add(self.m_serial_com_select, 1, wx.ALIGN_CENTER_VERTICAL)

        box_serial_parameter_bitrate = wx.BoxSizer(wx.HORIZONTAL)
        box_serial_parameter_bitrate.Add(self.m_serial_bitrate_title, 1, wx.ALIGN_CENTER_VERTICAL)
        box_serial_parameter_bitrate.Add(self.m_serial_bitrate_select, 1, wx.ALIGN_CENTER_VERTICAL)

        box_serial_parameter_databit = wx.BoxSizer(wx.HORIZONTAL)
        box_serial_parameter_databit.Add(self.m_serial_databit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        box_serial_parameter_databit.Add(self.m_serial_databit_select, 1, wx.ALIGN_CENTER_VERTICAL)

        box_serial_parameter_stopbit = wx.BoxSizer(wx.HORIZONTAL)
        box_serial_parameter_stopbit.Add(self.m_serial_stopbit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        box_serial_parameter_stopbit.Add(self.m_serial_stopbit_select, 1, wx.ALIGN_CENTER_VERTICAL)

        box_serial_parameter_checkbit = wx.BoxSizer(wx.HORIZONTAL)
        box_serial_parameter_checkbit.Add(self.m_serial_checkbit_title, 1, wx.ALIGN_CENTER_VERTICAL)
        box_serial_parameter_checkbit.Add(self.m_serial_checkbit_select, 1, wx.ALIGN_CENTER_VERTICAL)

        box_serial_parameter = wx.BoxSizer(wx.VERTICAL)
        box_serial_parameter.Add(box_serial_parameter_com, 1, wx.EXPAND)
        box_serial_parameter.Add(box_serial_parameter_bitrate, 1, wx.EXPAND)
        box_serial_parameter.Add(box_serial_parameter_databit, 1, wx.EXPAND)
        box_serial_parameter.Add(box_serial_parameter_stopbit, 1, wx.EXPAND)
        box_serial_parameter.Add(box_serial_parameter_checkbit, 1, wx.EXPAND)

        box_serial_serial = wx.GridSizer(3, 1)
        box_serial_serial.Add(self.m_serial_open_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        box_serial_serial.Add(self.m_serial_close_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        box_serial_serial.Add(self.m_program_exit_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)

        box_serial = wx.GridBagSizer()
        box_serial.Add(self.m_serial_title,     (0, 0), (1, 2), wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        box_serial.Add(box_serial_parameter,    (1, 0), (1, 1), wx.EXPAND)
        box_serial.Add(box_serial_serial,       (1, 1), (1, 1), wx.EXPAND)
        box_serial.AddGrowableRow(1, 1)
        box_serial.AddGrowableCol(0, 1)
        box_serial.AddGrowableCol(1, 1)


        box_action = wx.GridBagSizer()
        box_action.Add(self.m_action_title,                     (0, 0), (1, 4), wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_VERTICAL)
        box_action.Add(self.m_action_list,                      (1, 0), (1, 4), wx.EXPAND)
        box_action.Add(self.m_action_motor_step_select_title,   (2, 2), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        box_action.Add(self.m_action_motor_step_select,         (2, 3), (1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_action.Add(self.m_action_up_button,                 (3, 0), (1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_action.Add(self.m_action_down_button,               (3, 1), (1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_action.Add(self.m_action_edit_button,               (3, 2), (1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_action.Add(self.m_action_delete_button,             (3, 3), (1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_action.Add(self.m_action_add_button,                (4, 0), (1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_action.Add(self.m_action_save_button,               (4, 1), (1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_action.Add(self.m_action_load_button,               (4, 2), (1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_action.Add(self.m_action_send_button,               (4, 3), (1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        box_action.AddGrowableRow(1, 1)
        box_action.AddGrowableCol(0, 1)
        box_action.AddGrowableCol(1, 1)
        box_action.AddGrowableCol(2, 1)
        box_action.AddGrowableCol(3, 1)

        main_box = wx.GridSizer(0, 2)
        main_box.Add(box_recieve,   0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(box_serial,    0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(box_send,      0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(box_action,    0, wx.EXPAND | wx.ALL, 5)


        panel.SetSizer(main_box)
        panel.Layout()
        panel.Fit()
        #panel.Centre()

        #self.SetSizer(main_vbox)
        self.Layout()
        self.Fit()
        #self.Centre()


        # Connect Events
        self.m_recieve_clear_button.Bind(wx.EVT_BUTTON, self.on_recieve_clear_button_clicked)

        self.m_send_clear_button.Bind(wx.EVT_BUTTON, self.on_send_clear_button_clicked)
        self.m_send_button.Bind(wx.EVT_BUTTON, self.on_send_button_clicked)

        self.m_serial_open_button.Bind(wx.EVT_BUTTON, self.on_serial_open_button_clicked)
        self.m_serial_close_button.Bind(wx.EVT_BUTTON, self.on_serial_close_button_clicked)


        self.m_action_up_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_up_button_clicked)
        self.m_action_down_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_down_button_clicked)
        self.m_action_edit_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_edit_button_clicked)
        self.m_action_delete_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_delete_button_clicked)

        self.m_action_add_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_add_button_clicked)
        self.m_action_save_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_save_button_clicked)
        self.m_action_load_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_load_button_clicked)
        self.m_action_send_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_send_button_clicked)


        self.m_program_exit_button.Bind(wx.EVT_BUTTON, self.on_program_exit_button_clicked)


    # Recieve area update
    def on_recieve_area_update(self, data):
        s = data
        if self.m_hex_show_checkbox.IsChecked():
            s_trans = []
            for c in s:
                s_trans.append('%02X' % ord(c))

            #s = ''.join('%02X' %i for i in [ord(c) for c in s])

            self.m_recieve_area.AppendText(''.join(s_trans))
        else:
            self.m_recieve_area.AppendText(s)


            #s_trans = []
            #for i in range(0, len(s)/2):
            #    s_trans.append(chr(int(s[i*2:i*2+2], 16)))

            #s = ''.join([chr(int(i,16)) for i in [s[i*2:i*2+2] for i in range(0,len(s)/2)]])


    # Recieve area.
    def on_recieve_clear_button_clicked(self, event):
        self.m_recieve_area.Clear()

    # Send area.
    def on_send_clear_button_clicked(self, event):
        self.m_send_area.Clear()

    def on_send_button_clicked(self, event):
        try:
            if self.m_hex_send_checkbox.IsChecked():
                self.ser.write(self.m_send_input.GetValue().decode("hex"))
            else:
                self.ser.write(self.m_send_input.GetValue())

        except Exception, e:
            print '[serial_frame\t] Write Fail!!', e

        else:
            print '[serial_frame\t] Write Succeed!'
            self.m_send_area.AppendText(self.m_send_input.GetValue())
            self.m_send_input.Clear()


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
                print '[serial_frame\t] COMM Open Fail!!', e

            else:
                self.m_serial_open_button.Enable(False)
                self.m_serial_close_button.Enable(True)
        else:
            pass

            #self.ser.close()
            #while self.ser.isOpen(): pass

            #self.m_serial_open_button.SetLabel(u'打开串口')
            #self.m_imgStat.SetBitmap(Img_inclosing.getBitmap())

    def on_serial_close_button_clicked(self, event):
        if self.ser.isOpen():
            try:
                self.ser.close()
                while self.ser.isOpen():
                    pass

            except Exception, e:
                print '[serial_frame\t] COMM close Fail!!', e

            else:
                self.m_serial_open_button.Enable(True)
                self.m_serial_close_button.Enable(False)

        else:
            pass


    # Move designing area.
    def on_move_parameter_up_button_clicked(self, event):
        #action_list_index = self.m_action_list.GetFocusedItem()
        pass

    def on_move_parameter_down_button_clicked(self, event):
        #action_list_index = self.m_action_list.GetFocusedItem()
        pass

    def on_move_parameter_edit_button_clicked(self, event):
        pass

    def on_move_parameter_delete_button_clicked(self, event):
        action_index = self.m_action_list.GetFocusedItem()
        self.m_action_list.DeleteItem(action_index)

        del self.actions[action_index]

    def on_move_parameter_add_button_clicked(self, event):
        dia = move_parameter_dialog(self.functions)

        if dia.ShowModal() == wx.ID_OK:
            function = self.functions[dia.function_area_function_list_box.GetSelection()]

            action = []
            value_list = []
            action.append(function['function_name'])
            for one_dict in function['parameter']:
                index = function['parameter'].index(one_dict)
                value = dia.value_input[index].GetValue()
                action.append(value)
                value_list.append(one_dict['name'] + '=' + value)

            self.actions.append(action)
            action_index = self.m_action_list.GetItemCount()
            self.m_action_list.InsertStringItem(action_index, str(action_index + 1))
            self.m_action_list.SetStringItem(action_index, 1, function['verbose_name'])
            self.m_action_list.SetStringItem(action_index, 2, ', '.join(value_list))
            self.m_action_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.m_action_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.m_action_list.SetColumnWidth(2, wx.LIST_AUTOSIZE)

        dia.Destroy()

    def on_move_parameter_save_button_clicked(self, event):
        dlg = wx.FileDialog(self, message=u"保存文件", defaultDir=os.getcwd(), defaultFile="", wildcard='*', style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            #print(self.actions)
            with io.open(path, 'w', encoding='utf8') as f:
                #json.dump(self.actions, f, ensure_ascii=False, indent=4)
                data = json.dumps(self.actions, f, ensure_ascii=False, indent=4)
                f.write(unicode(data))

        dlg.Destroy()

    def on_move_parameter_load_button_clicked(self, event):
        dlg = wx.FileDialog(self, u"选择文件", os.getcwd(), "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            with io.open(path, 'r') as f:
                self.actions = json.load(f)

            self.m_action_list.DeleteAllItems()

            function_names = []
            for one_dict in self.functions:
                functions_names.append(one_dict['function_name'])

            for action in self.actions:
                index = function_names.index(action[0])

                value_list = []
                for i in action[1:]:
                    value_list.append(self.functions[index]['parameter']['name'] + '=' + action[i])

                action_index = self.m_action_list.GetItemCount()
                self.m_action_list.InsertStringItem(action_index, str(action_index + 1))
                self.m_action_list.SetStringItem(action_index, 1, self.functions[index]['parameter']['verbose_name'])
                self.m_action_list.SetStringItem(action_index, 2, ', '.join(value_list))
                self.m_action_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
                self.m_action_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
                self.m_action_list.SetColumnWidth(2, wx.LIST_AUTOSIZE)

        dlg.Destroy()


    def on_move_parameter_send_button_clicked(self, event):
        commands = []
        real_commands = []

        for action in self.actions:
            command = getattr(self, action[0])(action)
            commands.append(command)

        commands.append(['00', '00', '00',])

        for one_list in commands:
            real_commands.extend(one_list)

        print "[serial_frame\t] action list = %s" % (commands)
        print "[serial_frame\t] total_list = %s" % (' '.join(real_commands))
        print "[serial_frame\t] final_str  = %s" % (''.join(real_commands))

        try:
            self.ser.write(''.join(real_commands).decode("hex"))
        except Exception, e:
            print '[serial_frame\t] Write Fail!!', e

        else:
            print '[serial_frame\t] Write succeed!'
            


    # Program exit.
    def on_program_exit_button_clicked(self, event):
        self.Close()
        print "[serial_fram\t] Frame exit.exit."
        #self.Destroy()


    # Logic function.
    '''
    When distance is big than max step_distance in single cycle, we must do action
    more than one.

    One method is divide the convered distance in two interger number for
    step_distance and cycle times, the numbers is called factor. we also need to
    filter the factor so that they fit two variables' limit.  I come out a idea:
    divide the converted distance in two number, which their muliplity is mostly
    near the distance, then get max factor up to single cycle for that variable,
    the other one for cycle time. but we faced a problem that how to get the two
    numbers.

    The other one method is divide the converted distance, getting the times and
    left number. we use max variable value for single cycle, and the times number
    for count time to do one cycle action, then use the left number for variable
    value fro single cycle, and one for count time to complete another cycle action.
    That is to say, we must do two action.

    I think the later method is easier and clear than former.

    Time is dealed with same method.
    '''

    def move_distance(self, parameter):
        motor_step  = float(self.m_action_motor_step_select.GetValue())
        direct      = int(parameter[1])
        speed       = int(parameter[2])
        distance    = float(parameter[3])

        if direct == 1:
            a1 = 'F'
        else:
            a1 = '0'

        a2 = '%1X' % (int(round(speed / 5)))
        a3 = ''
        a4 = self.MIN_PERIOD
        a5 = ''

        total = int(round(distance / motor_step))
        cycle = int(total / 256)
        left =  total - cycle * 256

        if cycle > 0:
            if left != 0:
                a3 = 'FF'
                a5 = '%02X' % (cycle)

                a3_left = '%02X' % (left)
                a5_left = '01'
                return [a1, a2, a3, a4, a5, a1, self.DEFAULT_SPEED, self.MIN_DISTANCE, self.MIN_PERIOD,
                        a1, a2, a3_left, a4, a5_left, a1, self.DEFAULT_SPEED, self.MIN_DISTANCE, self.MIN_PERIOD,
                ]
            else:
                a3 = 'FF'
                a5 = '%02X' % (cycle)
                return [a1, a2, a3, a4, a5, a1, self.DEFAULT_SPEED, self.MIN_DISTANCE, self.MIN_PERIOD,]

        else:
            a3 = '%02X' % (total)
            a5 = '01'
            return [a1, a2, a3, a4, a5, a1, self.DEFAULT_SPEED, self.MIN_DISTANCE, self.MIN_PERIOD,]

    def classical_move(self, parameter):
        motor_step      = float(self.m_action_motor_step_select.GetValue())
        direct          = int(parameter[1])
        speed           = int(parameter[2])
        step_distance   = float(parameter[3])
        pause_time      = int(parameter[4])
        count           = int(parameter[5])

        # True point 'F', move up direct.
        if direct == 1:
            a1 = 'F'
        else:
            a1 = '0'

        a2 ='%1X' % (int(round(speed / 5)))
        a3 = '%02X' % (int(round(step_distance / motor_step)))
        a4 = '%02X%02X' % (int(pause_time / 256), (pause_time % 256))
        a5 = '%02X' % (count)

        return [a1, a2, a3, a4, a5, a1, self.DEFAULT_SPEED, self.MIN_DISTANCE, self.MIN_PERIOD,]

    def pause(self, parameter):
        motor_step  = float(self.m_action_motor_step_select.GetValue())
        time        = int(parameter[1])

        a1 = '0'
        a2 = self.DEFAULT_SPEED
        a3 = self.MIN_DISTANCE
        a4 = ''
        a5 = ''

        cycle = int(time / 65535)
        left =  time - cycle * 65535

        if cycle > 0:
            if left != 0:
                a4 = 'FFFF'
                a5 = '%02X' % (cycle)

                a4_left = '%02X%02X' % (int(left / 256), (left % 256))
                a5_left = '01'
                return [a1, a2, a3, a4, a5, a1, self.DEFAULT_SPEED, self.MIN_DISTANCE, self.MIN_PERIOD,
                        a1, a2, a3, a4_left, a5_left, a1, self.DEFAULT_SPEED, self.MIN_DISTANCE, self.MIN_PERIOD,
                ]
            else:
                a4 = 'FFFF'
                a5 = '%02X' % (cycle)
                return [a1, a2, a3, a4, a5, a1, self.DEFAULT_SPEED, self.MIN_DISTANCE, self.MIN_PERIOD,]

        else:
            a4 = '%02X%02X' % (int(left / 256), (left % 256))
            a5 = '01'
            return [a1, a2, a3, a4, a5, a1, self.DEFAULT_SPEED, self.MIN_DISTANCE, self.MIN_PERIOD,]


class serial_thread(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser

        self.event_stop = threading.Event()
        self.start()

    def run(self):
        while not self.event_stop.is_set():
            if self.ser.isOpen() and self.ser.inWaiting():
                text = self.ser.read(self.ser.inWaiting())
                wx.CallAfter(pub.sendMessage, 'update', data=text)

            time.sleep(0.01)

    def stop(self):
        self.event_stop.set()


class one_app(wx.App):
    def OnInit(self):
        # Serial create.
        self.ser = Serial()
        self.thread = serial_thread(self.ser)

        # Main frame.
        self.frame = serial_frame(self.ser)
        self.frame.Show()

        # Create a pubsub receiver
        pub.subscribe(self.frame.on_recieve_area_update, 'update')

        #print 'Have shown.'
        return True

    def OnExit(self):
        self.thread.stop()
        print "[one_app\t] serial_thread exit."


def main():
    app = one_app()
    app.MainLoop()

if __name__ == '__main__':
    main()
