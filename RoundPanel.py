from random import randint
from datetime import date
import pandas as pd
import time
import wx

class RoundPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.Hide()
        self.parent = parent
        self.round_line = 0
        self.user_line = 0
        self.accuracy = 0
        self.time_start = 0
        self.time_end = 0

    def round(self):
        self.Show()
        self.SetClientSize(self.parent.Size)
        self.time_start = time.time()
        self.SetOwnBackgroundColour(wx.Colour(60, 60, 60, 0))
        sizer_vertical = wx.BoxSizer(wx.VERTICAL)
        sizer_horizontal = wx.BoxSizer(wx.HORIZONTAL)

        font = wx.Font()
        font.SetFamily(wx.FONTFAMILY_MODERN)
        font.SetPointSize(15)

        txt_info = wx.StaticText(self,
                                 label="Repeat sentence the fastest you can!",
                                 style=wx.ALIGN_CENTER_HORIZONTAL)
        txt_info.SetFont(font)
        txt_info.SetForegroundColour(wx.Colour(240, 240, 240, 0))
        sizer_vertical.Add(txt_info, 0, wx.CENTER | wx.EXPAND, 0)

        font.SetPointSize(20)
        font.MakeBold()
        self.round_line = self.get_random_line()
        round_text = wx.StaticText(self,
                                   label=''.join(("Repeat:\n", self.round_line)),
                                   size=(wx.Size.GetWidth(self.Size), 60),
                                   style=wx.ALIGN_CENTER_HORIZONTAL)
        round_text.SetFont(font)
        round_text.SetBackgroundColour(wx.Colour(200, 200, 200, 0))
        sizer_vertical.Add(round_text, 0, wx.CENTER | wx.EXPAND, 0)

        sizer_vertical.AddSpacer(10)
        txt_boxinfo = wx.StaticText(self,
                                    label="Type here!",
                                    style=wx.ALIGN_CENTER_HORIZONTAL)
        sizer_vertical.Add(txt_boxinfo, 0, wx.CENTER | wx.EXPAND, 0)

        self.txt_box = wx.TextCtrl(self, size=(wx.Size.GetWidth(self.Size), 20))
        self.txt_box.SetBackgroundColour(wx.Colour(200, 200, 200, 0))
        sizer_horizontal.Add(self.txt_box, 1, wx.CENTER | wx.EXPAND, 1)
        sizer_vertical.Add(sizer_horizontal, 0, wx.CENTER | wx.EXPAND, 0)

        sizer_vertical.AddSpacer(40)
        next_button = wx.Button(self, label="next")
        sizer_vertical.Add(next_button, 0, wx.CENTER, 0)
        next_button.Bind(wx.EVT_BUTTON, self.compare)
        next_button.Bind(wx.EVT_BUTTON, self.next_button_on)

        sizer_vertical.AddSpacer(100)
        self.SetSizer(sizer_vertical)
        self.Layout()

    def compare(self, first, second):
        self.time_end = time.time()
        print(first, second)
        self.parent.play_panel.whole_time.append(self.time_end - self.time_start)
        score = 0
        first = [i for i in first]
        second = [i for i in second]
        lengfi = len(first)  # length of the first string
        lengse = len(second)  # length of the second string

        # We need to prevent out of index error by appending blank spaces
        while lengfi < lengse:
            first.append(" ")
            lengfi = len(first)

        while lengse < lengfi:
            second.append(" ")
            lengse = len(second)

        for i, j in zip(range(lengfi), range(lengse)):
            if first[i] == second[j]:
                score += 1
            elif i + 1 <= lengse - 1:
                if first[i + 1] == second[j]:
                    score += 0.5
                    i += 1
            elif i > 0:
                if first[i - 1] == second[j]:
                    score += (1 / 3)
                    i -= 1
        try:
            self.accuracy = score / lengfi
            self.parent.play_panel.accuracy.append(self.accuracy)
            self.write_score()
        except ZeroDivisionError:
            print("No phrase")
            return -1

    def write_score(self):
        with open("testing_input.txt", "a") as f:
            f.write(''.join((str(self.accuracy), "\n")))

    def next_button_on(self, event):
        self.compare(self.round_line, self.txt_box.GetValue())
        self.Hide()
        self.parent.play_panel.next()

    def get_random_line(self):
        level = self.parent.specs[2]
        index = randint(0, self.get_volume(level))
        try:
            with open(level, "r") as file:
                for i, line in enumerate(file):
                    if index == i:
                        line = line.split(';')
                        return line[1]
        except FileNotFoundError:
            wx.MessageBox("ERROR!\nCannot find storage file",
                          "Error", wx.OK | wx.ICON_ERROR)
            self.parent.Close()

    def get_volume(self, level_path):
        try:
            with open(level_path, "r") as file:
                volume = 0
                for line in file:
                    volume += 1

            return volume
        except FileNotFoundError:
            wx.MessageBox("ERROR!\nCannot find storage file",
                          "Error", wx.OK | wx.ICON_ERROR)
            self.parent.Close()


