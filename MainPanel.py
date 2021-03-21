from random import randint
from datetime import date
import pandas as pd
import time
import wx


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.SetClientSize(self.parent.Size)
        self._init_ui()
        self.Centre()

    def _init_ui(self):
        self.SetBackgroundColour(wx.WHITE)
        sizer_vertical = wx.BoxSizer(wx.VERTICAL)

        logo = wx.Image("Logo.bmp", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        logo_bit = wx.StaticBitmap(self, -1, logo,
                                   size=(logo.GetWidth(), logo.GetHeight()))
        sizer_vertical.Add(logo_bit, 0, wx.ALIGN_CENTER, 0)

        play_button = wx.Button(self, 0, "Play")
        sizer_vertical.Add(play_button, 0, wx.ALIGN_CENTER, 0)
        play_button.Bind(wx.EVT_BUTTON, self.change_to_play)

        play_button = wx.Button(self, 0, "Options")
        sizer_vertical.Add(play_button, 0, wx.ALIGN_CENTER, 0)
        play_button.Bind(wx.EVT_BUTTON, self.change_to_options)

        exit_button = wx.Button(self, 0, "Exit")
        sizer_vertical.Add(exit_button, 0, wx.ALIGN_CENTER)
        exit_button.Bind(wx.EVT_BUTTON, self.on_exit)

        self.SetSizerAndFit(sizer_vertical)

    def change_to_play(self, event):
        self.parent.switch_panel(self.parent.main_panel, self.parent.timer_panel)
        self.parent.timer_panel.SetClientSize(self.parent.Size)
        self.parent.timer_panel.timer_on()

    def change_to_options(self, event):
        self.parent.switch_panel(self.parent.main_panel, self.parent.option_panel)

    def on_exit(self, event):
        self.parent.Close(True)

