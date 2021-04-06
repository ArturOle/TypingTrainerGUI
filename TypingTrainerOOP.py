from random import randint
from datetime import date
import pandas as pd
import time
import wx
from MainPanel import *
from OptionsPanel import *
from PlayPanel import *
from RoundPanel import *
from TimerPanel import *
from HighscoresPanel import *


class Frame(wx.Frame):
    """
    Initialization of the program

    We initialize our main frame and all the panels

    switch_panel(static)- responsible for switching between the panels

    generate_rounds - generates queue of RoundPanels
                      in quantity given by the user in OptionPanel

    Structure:

                   ================ HighscoresPanel <=================
                  V                                                  |
    Frame => MainPanel-(Play) => TimerPanel => PlayPanel => {RoundPanels}
                  ^   -(Options) => OptionsPanel              ^       |
                  |   -(Close) => End.     |                  |       |
                  |                        |                   =======
                  ==========================
    """
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.width, self.height = wx.Window.GetClientSize(self)
        self.SetInitialSize((640, 480))
        self.main_panel = MainPanel(self)

        self.highscores_panel = HighscoresPanel(self)
        self.highscores_panel.Hide()

        self.timer_panel = TimerPanel(self)
        self.timer_panel.Hide()

        self.option_panel = OptionsPanel(self)
        self.option_panel.Hide()

        self.specs = self.option_panel.get_specs()["Value"]

        self.round_panels = self.generate_rounds()

        self.play_panel = PlayPanel(self)
        self.play_panel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.main_panel, 1, wx.EXPAND, 1)
        self.sizer.Add(self.timer_panel, 1, wx.EXPAND, 1)
        self.sizer.Add(self.play_panel, 1, wx.EXPAND, 1)
        self.sizer.Add(self.option_panel, 1, wx.EXPAND, 1)
        self.sizer.Add(self.highscores_panel,1, wx.EXPAND, 1)
        self.sizer.AddMany(([panel, 1, wx.EXPAND, 1] for panel in self.round_panels))

        self.SetSizer(self.sizer)

    @staticmethod
    def switch_panel(from_panel, to_panel):
        if from_panel.IsShown():
            from_panel.Hide()
        to_panel.Show()

    def generate_rounds(self):
        rounds = [RoundPanel(self) for panel in range(0, self.specs[1])]
        return rounds


def main():
    myapp = wx.App()
    frame = Frame(None, title="TypingTrainer2")
    frame.SetMinSize((640, 420))
    frame.Show()
    myapp.MainLoop()


if __name__ == "__main__":
    main()
