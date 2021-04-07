import wx
import pandas as pd
import wx.lib.plot.plotcanvas
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import datestr2num
from matplotlib import ticker
import matplotlib.dates as mdates
import datetime


class HighscoresPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.SetClientSize(self.parent.Size)
        self.v_box = wx.BoxSizer(wx.VERTICAL)
        self.grid_sizer = wx.GridSizer(6, 4, 3, 5)

        self.init_ui()

    def init_ui(self):
        self.v_box.AddStretchSpacer(1)
        self.highscores()
        self.panel()

        continue_button = wx.Button(self, 0, label="Continue")
        continue_button.Bind(wx.EVT_BUTTON, self.change_to_main)

        self.v_box.Add(continue_button, 1, wx.ALIGN_CENTER)
        self.v_box.AddStretchSpacer(1)
        self.SetSizerAndFit(self.v_box)

    def change_to_main(self, event):
        self.parent.switch_panel(self.parent.highscores_panel, self.parent.main_panel)
        self.parent.main_panel.SetClientSize(self.parent.Size)

    def panel(self):
        with open("Highscores.csv", newline='') as f:
            reader = csv.reader(f)
            data = np.array(list(reader)).transpose().tolist()
            print(data)
            for index in range(1, len(data[1])):
                data[2][index] = float(data[2][index])
        dates = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in data[1][1:]]
        dates_range = range(len(dates))
        plt.plot(dates_range, data[2][1:])
        plt.gcf().autofmt_xdate()
        plt.xticks(dates_range, dates)
        plt.show()

        plot = wx.lib.plot.PlotCanvas(self)

    def highscores(self):
        top_5 = pd.read_csv('Highscores.csv')\
            .sort_values("score", ascending=False)\
            .head(5)
        font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
        self.grid_sizer.AddMany([
            (wx.StaticText(self, label="Date:"), 0, wx.EXPAND | wx.CENTER),
            (wx.StaticText(self, label="Score:"), 0, wx.EXPAND | wx.CENTER),
            (wx.StaticText(self, label="Time:"), 0, wx.EXPAND | wx.CENTER),
            (wx.StaticText(self, label="Accuracy:"), 0, wx.EXPAND | wx.CENTER)
        ])

        for row in top_5.values:
            for data in list(row)[1:]:
                data = wx.StaticText(self, label=str(data))
                data.SetFont(font)
                self.grid_sizer.Add(data, 0, wx.EXPAND | wx.CENTER)

        self.v_box.Add(self.grid_sizer, proportion=1, flag=wx.EXPAND | wx.CENTER)






