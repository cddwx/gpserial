#!/usr/bin/env python
# coding=utf-8

import wx
import wx.xrc
from wx.lib.pubsub import pub as Publisher
from wx.lib import embeddedimage
from wx.lib import buttons

import json
import time
import os
import io
import threading
from serial import Serial
import serial.tools.list_ports


class move_parameter_dialog(wx.Dialog):
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

    def __init__(self):
        wx.Dialog.__init__(
                self,
                parent=None,
                id=wx.ID_ANY,
                title=u"运动参数设置",
                pos=wx.DefaultPosition,
                size=wx.DefaultSize,
        )

        # Function selection area.
        self.function_area_title = wx.StaticText(self, label=u"选择运动函数")

        function_verbose_names = []
        for element in self.functions:
            function_verbose_names.append(element['verbose_name'])

        self.function_area_function_list_box = wx.ListBox(self, choices=function_verbose_names, style=wx.LB_SINGLE)

        # Parameter setting area.
        self.function_description_title = wx.StaticText(self, label=u"函数描述")

        self.parameter_setting_title = wx.StaticText(self, label=u"函数参数设置")

        # Operation area.
        self.ok_button = wx.Button(self, wx.ID_OK, u"确认添加")
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, u"取消")

        # Arrangement.
        left_vbox = wx.BoxSizer(wx.VERTICAL)
        left_vbox.Add(self.function_area_title, 1)
        left_vbox.Add(self.function_area_function_list_box, 8)

        self.function_description_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.parameter_vbox = wx.BoxSizer(wx.VERTICAL)

        right_vbox = wx.BoxSizer(wx.VERTICAL)
        right_vbox.Add(self.function_description_title, 1)
        right_vbox.Add(self.function_description_hbox, 2, wx.EXPAND)
        right_vbox.Add(self.parameter_setting_title, 1)
        right_vbox.Add(self.parameter_vbox, 5, wx.EXPAND)

        up_hbox = wx.BoxSizer(wx.HORIZONTAL)
        up_hbox.Add(left_vbox, 1, wx.EXPAND)
        up_hbox.Add(right_vbox, 3, wx.EXPAND)

        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        bottom_hbox.Add(self.ok_button, 1)
        bottom_hbox.Add(self.cancel_button, 1)

        main_vbox = wx.BoxSizer(wx.VERTICAL)
        main_vbox.Add(up_hbox, 1, wx.EXPAND)
        main_vbox.Add(bottom_hbox, 0, wx.EXPAND)

        self.SetSizer(main_vbox)
        self.Layout()
        #self.Fit()

        # Connect Events
        self.function_area_function_list_box.Bind(wx.EVT_LISTBOX, self.on_function_area_function_list_box_selected)


    # Event handlers
    def on_function_area_function_list_box_selected(self, event):
        function = self.functions[self.function_area_function_list_box.GetSelection()]

        self.function_description_hbox.Clear(True)
        self.parameter_vbox.Clear(True)

        self.function_description = wx.TextCtrl(self, value=function['description'], style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.function_description_hbox.Add(self.function_description, 1)

        self.parameter_list =[]
        for parameter_dict in function['parameter']:
            # Create widgets using names from data, but failed.
            #self.%s = wx.StaticText(self, label=parameter_dict['verbose_name']) % (parameter_dict['name'] + '_title')
            #self.%s = wx.TextCtrl(self, value=parameter_dict['value']) % (parameter_dict['name'] + '_input')

            #self.%s = wx.BoxSizer(wx.HORIZONTAL) % (parameter_dict['name'] + '_hbox')
            #self.%s.Add(%s, 1) % (parameter_dict['name'] + '_hbox', parameter_dict['name'] + '_title')
            #self.%s.Add(%s, 1) % (parameter_dict['name'] + '_hbox', parameter_dict['name'] + '_input')

            #self.parameter_vbox.Add(self.%s, 1, wx.EXPAND) % (parameter_dict['name'] + '_hbox')

            one_dict = {}
            one_dict['title'] = wx.StaticText(self, label=parameter_dict['verbose_name'])
            one_dict['input'] = wx.TextCtrl(self, value=parameter_dict['value'])

            self.parameter_list.append(one_dict)

        for parameter_dict in self.parameter_list:
            self.parameter_hbox = wx.BoxSizer(wx.HORIZONTAL)
            self.parameter_hbox.Add(parameter_dict['title'], 1)
            self.parameter_hbox.Add(parameter_dict['input'], 1)

            self.parameter_vbox.Add(self.parameter_hbox, 0, wx.EXPAND)

        self.Layout()
        #self.Fit()


    #def on_ok_button_clicked(self, event):

    #def on_cancel_button_clicked(self, event):


class SerialFrame(wx.Frame):
    MIN_PERIOD = ['01', '02']
    MIN_SPEED = ''
    MAX_SPEED = ''

    actions = []


    def __init__(self):
        wx.Frame.__init__(
                self,
                parent=None,
                id=wx.ID_ANY,
                title=u"OUYANG Lab Simplediper (提拉机命令发送程序)",
                pos=wx.DefaultPosition,
                size=wx.DefaultSize,
        )

        #self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        #self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        #self.SetBackgroundColour(wx.SystemSettings.GetColour(addwx.SYS_COLOUR_WINDOWFRAME))

        panel = wx.Panel(self)

        # Recieve objects.
        self.m_recieve_area_title = wx.StaticText(panel, label=u"接收区")
        self.m_recieve_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.m_recieve_area_clear_button = wx.Button(panel, label=u"清空")


        # Send objects.
        self.m_send_area_title = wx.StaticText(panel, label=u"发送区")
        self.m_send_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.m_send_area_clear_button = wx.Button(panel, wx.ID_ANY, u"清除")
        self.m_send_input = wx.TextCtrl(panel)
        self.m_send_button = wx.Button(panel, label=u"发送")

        # Serial parameter setting.
        self.m_serial_parameter_title = wx.StaticText(panel, label=u"串口设置")

        self.m_serial_parameter_com_title = wx.StaticText(panel, label=u"通讯端口：")

        #m_com_choices = [ u"COM1", u"COM2", u"COM3", u"COM4", u"COM5", u"COM6", u"COM7", u"COM8", u"COM9" ]
        m_com_choices = []
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) > 0:
            for port in port_list:
                m_com_choices.append(port[0])
        else:
            m_com_choices = []

        self.m_serial_parameter_com_select = wx.ComboBox(panel, choices=m_com_choices, style=wx.CB_READONLY)


        self.m_serial_parameter_bitrate_title = wx.StaticText(panel, label=u"波特率：")

        m_bitrate_choices = [ u"2400", u"4800", u"9600", u"14400", u"19200", u"28800", u"57600" ]
        self.m_serial_parameter_bitrate_select = wx.ComboBox(panel, choices=m_bitrate_choices, style=wx.CB_READONLY)


        self.m_serial_parameter_databit_title = wx.StaticText(panel, label=u"数据位：")

        m_databit_choices = [ u"5", u"6", u"7", u"8" ]
        self.m_serial_parameter_databit_select = wx.ComboBox(panel, choices=m_databit_choices, style=wx.CB_READONLY)

        self.m_serial_parameter_checkbit_title = wx.StaticText(panel, label=u"校验位：")

        m_checkbit_choices = [ u"None", u"Odd", u"Even", u"One", u"Zero" ]
        self.m_serial_parameter_checkbit_select = wx.ComboBox(panel, choices=m_checkbit_choices, style=wx.CB_READONLY)


        self.m_serial_parameter_stopbit_title = wx.StaticText(panel, label=u"停止位：")

        m_stopbit_choices = [ u"1", u"2" ]
        self.m_serial_parameter_stopbit_select = wx.ComboBox(panel, choices=m_stopbit_choices, style=wx.CB_READONLY)

        self.m_hex_send_checkbox = wx.CheckBox(panel, label=u"HEX发送")
        self.m_hex_show_checkbox = wx.CheckBox(panel, label=u"HEX显示")

        self.m_serial_parameter_open_button = buttons.GenButton(panel, wx.ID_ANY, u"打开串口")
        self.m_serial_parameter_close_button = buttons.GenButton(panel, wx.ID_ANY, u"关闭串口")


        # Move parameter.
        self.m_move_parameter_area_title = wx.StaticText(panel, label=u"运动参数设置")

        self.m_move_parameter_area = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_HRULES)
        self.m_move_parameter_area.InsertColumn(0, u"运动类型", format=wx.LIST_FORMAT_LEFT)
        self.m_move_parameter_area.InsertColumn(1, u"运动参数", format=wx.LIST_FORMAT_LEFT)

        self.m_move_parameter_motor_step_select_title = wx.StaticText(panel, label=u"电机步长：")

        m_motor_step_choices = [ u"2.4", u"1.557" ]
        self.m_move_parameter_motor_step_select = wx.ComboBox(panel, choices=m_motor_step_choices, style=wx.CB_READONLY)

        self.m_move_parameter_up_button = wx.Button(panel, label=u"上移")
        self.m_move_parameter_down_button = wx.Button(panel, label=u"下移")
        self.m_move_parameter_delete_button = wx.Button(panel, label=u"删除")
        self.m_move_parameter_edit_button = wx.Button(panel, label=u"编辑")

        self.m_move_parameter_add_button = wx.Button(panel, label=u"添加运动")
        self.m_move_parameter_save_button = wx.Button(panel, label=u"保存运动")
        self.m_move_parameter_load_button = wx.Button(panel, label=u"打开文件")
        self.m_move_parameter_send_button = wx.Button(panel, label=u"发送指令")

        # Program operation.
        self.m_program_exit_button = wx.Button(panel, label=u"退出程序")


        # Arrangement.
        left_hbox11 = wx.BoxSizer(wx.HORIZONTAL)
        left_hbox11.Add(self.m_send_input,1)
        left_hbox11.Add(self.m_send_button, 0)
        left_hbox11.Add(self.m_send_area_clear_button, 0)

        left_vbox = wx.BoxSizer(wx.VERTICAL)
        left_vbox.Add(self.m_recieve_area_title, 1)
        left_vbox.Add(self.m_recieve_area, 6, wx.EXPAND)
        left_vbox.Add(self.m_recieve_area_clear_button, 1)
        left_vbox.Add(self.m_send_area_title, 1)
        left_vbox.Add(self.m_send_area, 6, wx.EXPAND)
        left_vbox.Add(left_hbox11, 1, wx.EXPAND)

        right_hbox11 = wx.BoxSizer(wx.HORIZONTAL)
        right_hbox11.Add(self.m_serial_parameter_com_title, 1)
        right_hbox11.Add(self.m_serial_parameter_com_select, 1)

        right_hbox12 = wx.BoxSizer(wx.HORIZONTAL)
        right_hbox12.Add(self.m_serial_parameter_bitrate_title, 1)
        right_hbox12.Add(self.m_serial_parameter_bitrate_select, 1)

        right_hbox13 = wx.BoxSizer(wx.HORIZONTAL)
        right_hbox13.Add(self.m_serial_parameter_databit_title, 1)
        right_hbox13.Add(self.m_serial_parameter_databit_select, 1)

        right_hbox14 = wx.BoxSizer(wx.HORIZONTAL)
        right_hbox14.Add(self.m_serial_parameter_stopbit_title, 1)
        right_hbox14.Add(self.m_serial_parameter_stopbit_select, 1)

        right_hbox15 = wx.BoxSizer(wx.HORIZONTAL)
        right_hbox15.Add(self.m_serial_parameter_checkbit_title, 1)
        right_hbox15.Add(self.m_serial_parameter_checkbit_select, 1)

        right_hbox16 = wx.BoxSizer(wx.HORIZONTAL)
        right_hbox16.Add(self.m_hex_show_checkbox, 1)
        right_hbox16.Add(self.m_hex_send_checkbox, 1)

        right_hbox17 = wx.BoxSizer(wx.HORIZONTAL)
        right_hbox17.Add(self.m_serial_parameter_open_button, 1)
        right_hbox17.Add(self.m_serial_parameter_close_button, 1)

        right_hbox21 = wx.BoxSizer(wx.HORIZONTAL)
        right_hbox21.Add(self.m_move_parameter_up_button, 1)
        right_hbox21.Add(self.m_move_parameter_down_button, 1)
        right_hbox21.Add(self.m_move_parameter_edit_button, 1)
        right_hbox21.Add(self.m_move_parameter_delete_button, 1)
        right_hbox21.Add(self.m_move_parameter_motor_step_select_title, 1)
        right_hbox21.Add(self.m_move_parameter_motor_step_select, 1)

        right_hbox22 = wx.BoxSizer(wx.HORIZONTAL)
        right_hbox22.Add(self.m_move_parameter_add_button, 1)
        right_hbox22.Add(self.m_move_parameter_save_button, 1)
        right_hbox22.Add(self.m_move_parameter_load_button, 1)
        right_hbox22.Add(self.m_move_parameter_send_button, 1)


        right_vbox = wx.BoxSizer(wx.VERTICAL)
        right_vbox.Add(self.m_serial_parameter_title, 1)
        right_vbox.Add(right_hbox11, 1, wx.EXPAND)
        right_vbox.Add(right_hbox12, 1, wx.EXPAND)
        right_vbox.Add(right_hbox13, 1, wx.EXPAND)
        right_vbox.Add(right_hbox14, 1, wx.EXPAND)
        right_vbox.Add(right_hbox15, 1, wx.EXPAND)
        right_vbox.Add(right_hbox16, 1, wx.EXPAND)
        right_vbox.Add(right_hbox17, 1, wx.EXPAND)
        right_vbox.Add(self.m_move_parameter_area_title, 1)
        right_vbox.Add(self.m_move_parameter_area, 5, wx.EXPAND)
        right_vbox.Add(right_hbox21, 1)
        right_vbox.Add(right_hbox22, 1)

        up_hbox = wx.BoxSizer(wx.HORIZONTAL)
        up_hbox.Add(left_vbox, 1, wx.EXPAND)
        up_hbox.Add(right_vbox, 1, wx.EXPAND)

        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        bottom_hbox.Add(self.m_program_exit_button, 0)

        main_vbox = wx.BoxSizer(wx.VERTICAL)
        main_vbox.Add(up_hbox, 1, wx.EXPAND)
        main_vbox.Add(bottom_hbox, 0, wx.EXPAND)


        panel.SetSizer(main_vbox)
        #panel.Centre()
        panel.Layout()
        panel.Fit()

        #self.Centre()
        self.Layout()
        self.Fit()

        # Connect Events
        self.m_recieve_area_clear_button.Bind(wx.EVT_BUTTON, self.on_recieve_area_clear_button_clicked)

        self.m_send_area_clear_button.Bind(wx.EVT_BUTTON, self.on_send_area_clear_button_clicked)
        self.m_send_button.Bind(wx.EVT_BUTTON, self.on_send_button_clicked)

        self.m_serial_parameter_open_button.Bind(wx.EVT_BUTTON, self.on_serial_parameter_open_button_clicked)
        self.m_serial_parameter_close_button.Bind(wx.EVT_BUTTON, self.on_serial_parameter_close_button_clicked)


        self.m_move_parameter_up_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_up_button_clicked)
        self.m_move_parameter_down_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_down_button_clicked)
        self.m_move_parameter_edit_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_edit_button_clicked)
        self.m_move_parameter_delete_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_delete_button_clicked)

        self.m_move_parameter_add_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_add_button_clicked)
        self.m_move_parameter_save_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_save_button_clicked)
        self.m_move_parameter_load_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_load_button_clicked)
        self.m_move_parameter_send_button.Bind(wx.EVT_BUTTON, self.on_move_parameter_send_button_clicked)


        self.m_program_exit_button.Bind(wx.EVT_BUTTON, self.on_program_exit_button_clicked)

        # Serial create.
        self.Ser = Serial()
        self.serialThread = SerialThread(self.Ser)

        # Create a pubsub receiver
        Publisher.subscribe(self.on_recieve_area_update, 'update')

    # Recieve area update
    def on_recieve_area_update(self, msg):
        s = msg.data
        if self.m_hex_show_checkbox.IsChecked():
            s_trans = []
            for c in s:
                s_trans.append('%02X' % ord(c))

            #s = ''.join('%02X' %i for i in [ord(c) for c in s])
        else:
            s_trans = []
            for i in range(0, len(s)/2):
                s_trans.append(chr(int(s[i*2:i*2+2], 16)))

            #s = ''.join([chr(int(i,16)) for i in [s[i*2:i*2+2] for i in range(0,len(s)/2)]])

        self.m_recieve_area.AppendText(''.join(s_trans))


    # Recieve area.
    def on_recieve_area_clear_button_clicked(self, event):
        self.m_recieve_area.Clear()

    # Send area.
    def on_send_area_clear_button_clicked(self, event):
        self.m_send_area.Clear()

    def on_send_button_clicked(self, event):
        if self.m_hex_send_checkbox.IsChecked():
            self.Ser.write(self.m_send_input.GetValue().decode("hex"))

        else:
            self.Ser.write(self.m_send_input.GetValue())
            self.m_send_area.AppendText(self.m_send_input.GetValue())

        self.m_send_input.Clear()


    # Parameter setting area.
    def on_serial_parameter_open_button_clicked(self, event):
        if not self.Ser.isOpen():
            try:
                self.Ser.timeout = 1
                self.Ser.xonxoff = 0
                self.Ser.port = self.m_serial_parameter_com_select.GetValue()
                self.Ser.parity = self.m_serial_parameter_checkbit_select.GetValue()[0]
                self.Ser.baudrate = int(self.m_serial_parameter_bitrate_select.GetValue())
                self.Ser.bytesize = int(self.m_serial_parameter_databit_select.GetValue())
                self.Ser.stopbits = int(self.m_serial_parameter_stopbit_select.GetValue())
                self.Ser.open()
            except Exception,e:
                print 'COMM Open Fail!!',e

            else:
                self.m_serial_parameter_close_button.Enable(True)
        else:
            pass

            #self.Ser.close()
            #while self.Ser.isOpen(): pass

            #self.m_serial_parameter_open_button.SetLabel(u'打开串口')
            #self.m_imgStat.SetBitmap(Img_inclosing.getBitmap())

    def on_serial_parameter_close_button_clicked(self, event):
        if self.Ser.isOpen():
            try:
                self.Ser.close()
                while self.Ser.isOpen():
                    pass

            except Exception, e:
                print 'COMM close Fail!!', e

            else:
                self.m_serial_parameter_open_button.Enable(True)

        else:
            pass


    # Move designing area.
    def on_move_parameter_up_button_clicked(self, event):
        #action_index = self.m_move_parameter_area.GetFocusedItem()
        pass

    def on_move_parameter_down_button_clicked(self, event):
        #action_index = self.m_move_parameter_area.GetFocusedItem()
        pass

    def on_move_parameter_edit_button_clicked(self, event):
        pass

    def on_move_parameter_delete_button_clicked(self, event):
        action_index = self.m_move_parameter_area.GetFocusedItem()
        self.m_move_parameter_area.DeleteItem(action_index)

        del self.actions[action_index]

    def on_move_parameter_add_button_clicked(self, event):
        dia = move_parameter_dialog()
        if dia.ShowModal() == wx.ID_OK:
            function = dia.functions[dia.function_area_function_list_box.GetSelection()]

            action = {}
            action['function_name'] = function['function_name']
            action['verbose_name'] = function['verbose_name']
            action['parameter'] = []
            for parameter_dict in function['parameter']:
                index = function['parameter'].index(parameter_dict)
                one_dict = {}
                one_dict['name'] = parameter_dict['name']
                one_dict['value'] = dia.parameter_list[index]['input'].GetValue()
                action['parameter'].append(one_dict)

            self.actions.append(action)

            action_index = self.m_move_parameter_area.GetItemCount()
            self.m_move_parameter_area.InsertStringItem(action_index, action['verbose_name'])

            value_list = []
            for one_dict in action['parameter']:
                value_list.append(one_dict['value'])

            self.m_move_parameter_area.SetStringItem(action_index, 1, ', '.join(value_list))
            #print(self.actions)
            #print(value_list)

        dia.Destroy()

    def on_move_parameter_save_button_clicked(self, event):
        dlg = wx.FileDialog(self, message=u"保存文件", defaultDir=os.getcwd(), defaultFile="", wildcard='*', style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            #self.SetStatusText(u'你选择了: %s\n' % dlg.GetPath())

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
            #mypath = os.path.basename(path)
            #self.SetStatusText(u"你选择了: %s" % mypath)

            with io.open(path, 'r') as f:
                self.actions = json.load(f)

            self.m_move_parameter_area.DeleteAllItems()
            for action in self.actions:
                action_index = self.m_move_parameter_area.GetItemCount()

                self.m_move_parameter_area.InsertStringItem(action_index, action['verbose_name'])

                value_list = []
                for one_dict in action['parameter']:
                    value_list.append(one_dict['value'])

                #print(value_list)
                self.m_move_parameter_area.SetStringItem(action_index, 1, ', '.join(value_list))

        dlg.Destroy()


    def on_move_parameter_send_button_clicked(self, event):
        real_commands = []

        for action in self.actions:
            real_command = getattr(self, action['function_name'])(action['parameter'])
            real_commands.append(real_command)

        real_command.append('00 00 00')

        print(real_commands)

        self.Ser.write(' '.join(real_commands.decode("hex")))


    # Program exit.
    def on_program_exit_button_clicked(self, event):
        self.Close(True)


    # Logic function.
    '''
a12 range[0, 15]
Speed range [motor_step/3, infinite).

a2 range [0, 255]
distance range [0, 255*motor_step].

(a3 + a4) range [0('00 00'), 65535('FF FF')] ([258('01 02'), 65535(FF FF)])
pause_time range [0, 65535].

a5 range [0, 255] ([0, 255])
count range [0, 255] ([0, 255])
    '''
    def move_distance(self, parameter):
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
        '''
        motor_step  = float(self.m_move_parameter_motor_step_select.GetValue())
        direct      = parameter['direct']
        speed       = int(parameter['speed'])
        distance    = int(parameter['distance'])

        if parameter['direct'] == True:
            a11 = 'F'
        else:
            a11 = '0'

        a12 = '%1X' % (5 * int(motor_step / speed))
        a2 = ''
        a3 = self.MIN_PERIOD[0]
        a4 = self.MIN_PERIOD[1]
        a5 = ''

        total = int(distance / motor_step)
        cycle = int(total / 255)
        left =  total - cycle * 255

        if cycle > 0:
            if left != 0:
                a2 = 'FF'
                a5 = '%02X' % (cycle)

                a2_left = '%02X' % (left)
                a5_left = '01'
                return [a11 + a12, a2, a3, a4, a5, a11 + a12, '00', '01', '02',
                        a11 + a12, a2_left, a3, a4, a5_left, a11 + a12, '00', '01', '02',
                ]
            else:
                a2 = 'FF'
                a5 = '%02X' % (cycle)
                return [a11 + a12, a2, a3, a4, a5, a11 + a12, '00', '01', '02']

        else:
            a2 = '%02X' % (total)
            a5 = '01'
            return [a11 + a12, a2, a3, a4, a5, a11 + a12, '00', '01', '02']

    def classical_move(self, parameter):
        motor_step      = float(self.m_move_parameter_motor_step_select.GetValue())
        direct          = parameter['direct']
        speed           = int(parameter['speed'])
        step_distance   = int(parameter['step_distance'])
        pause_time      = int(parameter['pause_time'])
        count           = int(parameter['count'])

        # True point 'F', move up direct.
        if parameter['direct'] == True:
            a11 = 'F'
        else:
            a11 = '0'

        a12 ='%1X' % (5 * int(motor_step / speed))
        a2 = '%02X' % (int(step_distance / motor_step))
        a3 = '%02X' % (pause_time / 256)
        a4 = '%02X' % (pause_time % 256)
        a5 = '%02X' % (count)

        return [a11 + a12, a2, a3, a4, a5, a11 + a12, '00', '01', '02']

    def pause(self, parameter):
        motor_step  = int(self.m_move_parameter_motor_select.GetValue())
        time        = int(parameter['time'])

        if parameter['direct'] == True:
            a11 = 'F'
        else:
            a11 = '0'

        a12 = '%1X' % (5 * int(motor_step / speed))
        a2 = '00'
        a3 = ''
        a4 = ''
        a5 = ''

        cycle = int(time / 65535)
        left =  time - cycle * 65535

        if cycle > 0:
            if left != 0:
                a3 = 'FF'
                a4 = 'FF'
                a5 = '%02X' % (cycle)

                a3_left = '%02X' % (left / 256)
                a4_left = '%02X' % (left % 256)
                a5_left = '01'
                return [a11 + a12, a2, a3, a4, a5, a11 + a12, '00', '01', '02',
                        a11 + a12, a2, a3_left, a4_left, a5_left, a11 + a12, '00', '01', '02',
                ]
            else:
                a3 = 'FF'
                a4 = 'FF'
                a5 = '%02X' % (cycle)
                return [a11 + a12, a2, a3, a4, a5, a11 + a12, '00', '01', '02']

        else:
            a3 = '%02X' % (left / 256)
            a4 = '%02X' % (left % 256)
            a5 = '01'
            return [a11 + a12, a2, a3, a4, a5, a11 + a12, '00', '01', '02']


class SerialThread(threading.Thread):
    def __init__(self, Ser):
        super(SerialThread, self).__init__()
        #threading.Thread.__init__()
        self.Ser = Ser
        self.start()

    def run(self):
        while True:
            if self.Ser.isOpen() and self.Ser.inWaiting():
                text = self.Ser.read(self.Ser.inWaiting())
                wx.CallAfter(Publisher.sendMessage('update', text))

            time.sleep(0.01)

Img_inclosing = embeddedimage.PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAIAAAAC64paAAAAAXNSR0IArs4c6QAAAARnQU1B"
    "AACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABiSURBVDhPY/iPDTBgAOzK0EQxtSGL"
    "oCtG5uPXCZFFUQ/nEKMTTT/UJOJ1IusHaSZVJ1z/AGkmz70jXBfZ8QxNq+QFH8hWsm2GaiZD"
    "PyQ7IbIY8Y5HZETq5GeoS/A6AK0kAQCtTO8ROTKfPAAAAABJRU5ErkJggg==")


Img_inopening = embeddedimage.PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B"
    "AACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAACKSURBVDhPY/wPBAw4wDtZVawyQo9v"
    "49LCwIjNQFwGoZuCzWAmdEXEGgbSh00tioGkGAZzCLoeuIHkGIbNULCBlBiGbihGGOKMPiIl"
    "qGogyKeMb2VUcKZDIh2FooyqLgSZPBINxJfRBzxSQI6jTaRQw9swM+AupMRQZL0oXibHUHQ9"
    "GGFIiqHY1AIAg2UtGigTDxsAAAAASUVORK5CYII=")


class simplediper(wx.App):
    def OnInit(self):
        self.frame = SerialFrame()
        self.frame.Show(True)

        #print 'Have shown.'
        return True


if __name__ == '__main__':
    app = simplediper()
    app.MainLoop()

