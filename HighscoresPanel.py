import wx
import pandas as pd


class HighscoresPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.SetClientSize(self.parent.Size)
        self.v_box = wx.BoxSizer(wx.VERTICAL)

        self.init_ui()

    def init_ui(self):
        self.v_box.AddStretchSpacer(1)
        self.highscores()
        continue_button = wx.Button(self, 0, label="Continue")
        continue_button.Bind(wx.EVT_BUTTON, self.change_to_main)

        self.v_box.Add(continue_button, 1, wx.ALIGN_CENTER)
        self.v_box.AddStretchSpacer(1)
        self.SetSizerAndFit(self.v_box)

    def change_to_main(self, event):
        self.parent.switch_panel(self.parent.highscores_panel, self.parent.main_panel)
        self.parent.main_panel.SetClientSize(self.parent.Size)

    def highscores(self):
        top_5 = pd.read_csv('Highscores.csv')\
            .sort_values("score", ascending=False)\
            .head(5)

        for row in top_5.values:
            self.v_box.Add(wx.StaticText(self, label=''.join(str(row[1:]).split(','))[1:-1]), 1, wx.ALIGN_CENTER)









