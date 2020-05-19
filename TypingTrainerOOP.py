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

        logo = wx.Image("logo.bmp", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
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
        sizer_vertical.Add(exit_button, 0, wx.ALIGN_CENTRE)
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


class OptionsPanel(wx.Panel):
    """
    Options

    In initialization we're creating the screen with all it's components
    and display informations saved in options.json

    get_specs(static) - responsible for extracting informations from options.json in shape of dictionary

    overwrite_specs(private) - responsible for updating options.json with specifications chosen by the user
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.SetSize((640, 480))
        self.width = self.Size[0]
        self.parent = parent
        self.SetClientSize(self.parent.Size)

        self.SetOwnBackgroundColour(wx.Colour(255, 255, 255, 0))

        sizer_vertical = wx.BoxSizer(wx.VERTICAL)
        sizer_horizontal = wx.BoxSizer(wx.HORIZONTAL)

        specs = self.get_specs()

        sizer_vertical.AddSpacer(20)
        sizer_horizontal.Add(wx.StaticText(self, label="Quantity of rounds"))
        sizer_vertical.Add(sizer_horizontal, 0, wx.CENTER, 0)

        self.rounds_slider = wx.Slider(self,
                                       value=specs["Value"][1],
                                       minValue=1,
                                       maxValue=10,
                                       style=wx.SL_HORIZONTAL | wx.SL_LABELS,
                                       size=(self.width-15, 20))
        sizer_vertical.Add(self.rounds_slider, flag=wx.CENTER | wx.TOP | wx.EXPAND)
        self.rounds_slider.Bind(wx.EVT_SCROLL, self.Update())

        self.box_text = wx.StaticText(self, label="Choose difficulty")
        sizer_vertical.AddSpacer(40)
        sizer_vertical.Add(self.box_text, 0, wx.CENTER, 0)

        self.level_box = wx.ComboBox(self,
                                     choices=("Medium", "High"),
                                     style=wx.CB_READONLY)
        self.level_box.SetValue(specs["Value"][0])
        sizer_vertical.AddSpacer(10)
        sizer_vertical.Add(self.level_box, 0, wx.CENTER, 0)

        self.path_text = wx.StaticText(self, label="Storage directory")
        sizer_vertical.AddSpacer(30)
        sizer_vertical.Add(self.path_text, 0, wx.CENTER, 0)

        self.path = wx.StaticText(self,
                                  size=(wx.Size.GetWidth(self.Size), 20),
                                  style=wx.ALIGN_CENTER_HORIZONTAL)
        self.path.Label = specs["Value"][2]
        sizer_vertical.AddSpacer(10)
        sizer_vertical.Add(self.path, 0, wx.CENTER, 0)

        save_button = wx.Button(self, label="Save Changes")
        save_button.Bind(wx.EVT_BUTTON, self._overwrite_specs)
        sizer_vertical.AddSpacer(100)
        sizer_vertical.Add(save_button, 0, wx.CENTER | wx.BOTTOM, 0)

        specs = self.get_specs()
        print(specs["Option"][1])
        print(specs["Value"][1])

        sizer_vertical.AddSpacer(2000)

        self.SetSizerAndFit(sizer_vertical)
        self.Layout()

    @staticmethod
    def get_specs():
        df = pd.read_json("options.json")
        dictionary = df.to_dict()
        return dictionary

    def _overwrite_specs(self, event):
        value_level = self.level_box.GetValue()
        value_rounds = self.rounds_slider.GetValue()

        if self.get_specs()["Value"][0][0] == "M":
            value_patch = "storageM.csv"
        else:
            value_patch = "storageM.csv"

        print("Option 1 changed to ", value_rounds)
        df = pd.read_json("options.json")
        df.iloc[0, 1] = value_level
        df.iloc[1, 1] = value_rounds
        print("Current state: \n", df)
        df.to_json("options.json")

        self.parent.specs = self.get_specs()["Value"]
        self.parent.round_panels = self.parent.generate_rounds()
        self.parent.switch_panel(self.parent.option_panel, self.parent.main_panel)
        self.parent.main_panel.SetClientSize(self.parent.Size)


class Frame(wx.Frame):
    """
    Initialization of the program

    We initialize our main frame and all the panels

    switch_panel(static)- responsible for switching between the panels

    generate_rounds - generates queue of RoundPanels
                      in quantity given by the user in OptionPanel

    Structure:

                   ===================================================
                  V                                                  \
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
