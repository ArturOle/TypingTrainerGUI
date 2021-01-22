from random import randint
from datetime import date
import pandas as pd
import time
import wx

class PlayPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.current_round = 0
        self.score = 0
        self.accuracy = []
        self.whole_time = []

    def game(self):
        if self.current_round < self.parent.specs[1]:
            self.parent.switch_panel(self, self.parent.round_panels[self.current_round])
            self.parent.round_panels[self.current_round].round()
        else:
            self.parent.main_panel.SetClientSize(self.parent.Size)
            self.parent.main_panel.Show()
            self.gen_highscore()
            self.current_round = 0
            self.accuracy = []
            self.whole_time = []

    def next(self):
        self.current_round += 1
        self.game()

    def gen_highscore(self):
        self.whole_time = sum(self.whole_time)
        self.accuracy = sum(self.accuracy)/len(self.accuracy)
        print(self.whole_time)
        print(self.accuracy)
        self.score = '{0:.2f}'.format((self.parent.specs[1]
                                       * 100000
                                       * (pow(self.accuracy, 2))/self.whole_time))
        print(self.score)
        self.to_csv()

    def to_csv(self):
        data = {"date": [str(date.today())],
                "score": [self.score],
                "time": [self.whole_time],
                "accuracy": [self.accuracy]}

        new_data = pd.DataFrame(data)
        # df = df.append(new_data, ignore_index=True)
        new_data.to_csv("Highscores.csv", mode='a', header=False)
        print(pd.read_csv('Highscores.csv'))