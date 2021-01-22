from random import randint
from datetime import date
import pandas as pd
import time
import wx

class TimerPanel(wx.Panel):
    """
    Timer

    Creates transitional screen between MainPanel and PlayPanel
    with counter.

    timer_method - responsible for functionalities of the counter

    timer_on - starts counter

    timer_off - stops counter
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.SetOwnBackgroundColour(wx.Colour(60, 60, 60, 0))
        self.sizer_vertical = wx.BoxSizer(wx.VERTICAL)

        self.time_remaining = 3
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_method, self.timer)

        self.sizer_vertical.AddSpacer(40)

        font = wx.Font()

        font.SetPointSize(30)
        self.info_text = wx.StaticText(self,
                                       label="Prepare for typing!",
                                       style=wx.ALIGN_CENTER,
                                       size=(wx.Size.GetWidth(self.parent.Size), 100))
        self.info_text.SetFont(font)
        self.sizer_vertical.Add(self.info_text, 0, wx.CENTER, 0)

        font.SetPointSize(100)
        self.counter_text = wx.StaticText(self,
                                          style=wx.ALIGN_CENTER,
                                          size=(wx.Size.GetWidth(self.parent.Size), 100))
        self.counter_text.SetFont(font)
        self.sizer_vertical.Add(self.counter_text, 0, wx.CENTER, 0)

        self.SetSizer(self.sizer_vertical)
        self.Layout()

        if self.time_remaining <= 0:
            self.timer_off()

    def timer_method(self, event):
        if self.time_remaining < 0:
            self.time_remaining = 3
            self.timer_off()
            self.parent.switch_panel(self, self.parent.play_panel)
            self.parent.play_panel.game()
            self.counter_text.SetLabel(label=str(self.time_remaining))
        else:
            counter_text = str(self.time_remaining)
            self.counter_text.SetLabel(label=counter_text)
            self.time_remaining -= 1

    def timer_on(self):
        self.timer.Start(1000)

    def timer_off(self):
        self.timer.Stop()
