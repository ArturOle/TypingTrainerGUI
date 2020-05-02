from random import randint
import pandas as pd
import wx


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.height = wx.Window.GetClientSize
        self.parent = parent
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
        self.parent.switch_panel(self.parent.main_panel, self.parent.play_panel)
        self.parent.play_panel.timer_on()

    def change_to_options(self, event):
        self.parent.switch_panel(self.parent.main_panel, self.parent.option_panel)

    def on_exit(self, event):
        self.parent.Close(True)


class PlayPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.SetSize((640, 420))
        self.parent = parent
        self.SetOwnBackgroundColour(wx.Colour(60, 60, 60, 0))
        self.sizer_vertical = wx.BoxSizer(wx.VERTICAL)

        self.time_remaining = 5
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_method, self.timer)

        font = wx.Font()

        self.sizer_vertical.AddSpacer(40)

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
                                          size=(wx.Size.GetWidth(self.Size), 100))
        self.counter_text.SetFont(font)
        self.sizer_vertical.Add(self.counter_text, 0, wx.CENTER, 0)

        self.SetSizer(self.sizer_vertical)
        self.Layout()

        if self.time_remaining <= 0:
            self.timer_off()

    def timer_method(self, event):
        if self.time_remaining < 0:
            self.timer_off()
            self.clean()
            self.game(5)
        else:
            counter_text = str(self.time_remaining)
            self.counter_text.SetLabel(label=counter_text)
            self.Update()
            self.time_remaining -= 1

    def clean(self):
        for child in self.GetChildren():
            child.Destroy()

    def timer_on(self):
        self.timer.Start(1000)

    def timer_off(self):
        self.timer.Stop()

    def game(self, nr_of_rounds):
        while nr_of_rounds > 0:
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
            sizer_vertical.Add(txt_info, 0, wx.CENTER, 0)

            font.SetPointSize(20)
            font.MakeBold()
            round_line = self.get_random_line()
            round_text = wx.StaticText(self,
                                       label=''.join(("Repeat:\n", round_line)),
                                       size=(wx.Size.GetWidth(self.Size), 60),
                                       style=wx.ALIGN_CENTER_HORIZONTAL)
            round_text.SetFont(font)
            round_text.SetBackgroundColour(wx.Colour(200, 200, 200, 0))
            sizer_vertical.Add(round_text, 0, wx.CENTER, 0)

            sizer_vertical.Add((0, 10), 0, wx.CENTER, 0)

            txt_box = wx.TextCtrl(self, size=(wx.Size.GetWidth(self.Size), 20))
            txt_box.SetBackgroundColour(wx.Colour(200, 200, 200, 0))
            sizer_horizontal.Add(txt_box, 1, wx.EXPAND, 1)

            sizer_vertical.Add(sizer_horizontal, 0, wx.CENTER, 0)
            sizer_vertical.AddSpacer(100)
            self.SetSizer(sizer_vertical)
            self.Layout()
            nr_of_rounds -= 1

    def get_random_line(self):
        index = randint(0, self.get_volume())
        try:
            with open("storageM.csv", "r") as file:
                for i, line in enumerate(file):
                    if index == i:
                        line = line.split(';')
                        return line[1]
        except FileNotFoundError:
            wx.MessageBox("ERROR!\nCannot find storage file",
                          "Error", wx.OK | wx.ICON_ERROR)
            self.parent.Close()

    def get_volume(self):
        try:
            with open("storageM.csv", "r") as file:
                volume = 0
                for line in file:
                    volume += 1

            return volume
        except FileNotFoundError:
            wx.MessageBox("ERROR!\nCannot find storage file",
                          "Error", wx.OK | wx.ICON_ERROR)
            self.parent.Close()


class OptionsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.SetSize((640, 480))
        self.width = self.Size[0]
        self.parent = parent
        self.SetSize((parent.width, parent.height))

        self.SetOwnBackgroundColour(wx.Colour(255, 255, 255, 0))

        sizer_vertical = wx.BoxSizer(wx.VERTICAL)
        sizer_horizontal = wx.BoxSizer(wx.HORIZONTAL)

        specs = self._get_specs()

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

        self.level_box = wx.ComboBox(self, choices=("Medium", "High"), style=wx.CB_READONLY)
        self.level_box.SetValue(specs["Value"][0])
        sizer_vertical.AddSpacer(10)
        sizer_vertical.Add(self.level_box, 0, wx.CENTER, 0)

        self.path_text = wx.StaticText(self, label="Storage directory")
        sizer_vertical.AddSpacer(30)
        sizer_vertical.Add(self.path_text, 0, wx.CENTER, 0)

        self.path_control = wx.TextCtrl(self, size=(wx.Size.GetWidth(self.Size), 20))
        self.path_control.SetValue(specs["Value"][2])
        sizer_vertical.AddSpacer(10)
        sizer_vertical.Add(self.path_control, 0, wx.CENTER, 0)

        save_button = wx.Button(self, label="Save Changes")
        save_button.Bind(wx.EVT_BUTTON, self._overwrite_specs)
        sizer_vertical.AddSpacer(100)
        sizer_vertical.Add(save_button, 0, wx.CENTER | wx.BOTTOM, 0)

        specs = self._get_specs()
        print(specs["Option"][1])
        print(specs["Value"][1])

        sizer_vertical.AddSpacer(2000)

        self.SetSizerAndFit(sizer_vertical)
        self.Layout()

    @staticmethod
    def _get_specs():
        df = pd.read_json("options.json")
        dictionary = df.to_dict()
        return dictionary

    def _overwrite_specs(self, event):
        value_level = self.level_box.GetValue()
        value_rounds = self.rounds_slider.GetValue()
        value_patch = "storageM.csv"
        print("Option 1 changed to ", value_rounds)
        df = pd.read_json("options.json")
        print(df)
        df.iloc[0, 1] = value_level
        df.iloc[1, 1] = value_rounds
        df.iloc[2, 1] = value_patch
        df.to_json("options.json")
        self.parent.switch_panel(self.parent.option_panel, self.parent.main_panel)


class Frame(wx.Frame):
    """ Initialization of the program

    We initialize our main frame and all the panels
    ,also create conditionality of when and which panel
    should be shown or hide.
    """
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.width, self.height = wx.Window.GetClientSize(self)
        self.main_panel = MainPanel(self)

        self.play_panel = PlayPanel(self)
        self.play_panel.Hide()

        self.option_panel = OptionsPanel(self)
        self.option_panel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.main_panel, 1, wx.EXPAND, 1)
        self.sizer.Add(self.play_panel, 1, wx.EXPAND, 1)
        self.sizer.Add(self.option_panel, 1, wx.EXPAND, 1)

        self.SetSizer(self.sizer)

    @staticmethod
    def switch_panel(from_panel, to_panel):
        if from_panel.IsShown():
            from_panel.Hide()
            to_panel.Show()


def main():
    myapp = wx.App()
    frame = Frame(None, title="TypingTrainer2")
    frame.SetMinSize((640, 420))
    frame.Show()
    myapp.MainLoop()


if __name__ == "__main__":
    main()
