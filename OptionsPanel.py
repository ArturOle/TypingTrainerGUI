from random import randint
from datetime import date
import pandas as pd
import time
import wx

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

        self.rounds_slider = wx.Slider(
            self,
            value=specs["Value"][1],
            minValue=1,
            maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS,
            size=(self.width-15, 20)
        )
        sizer_vertical.Add(self.rounds_slider, flag=wx.CENTER | wx.TOP | wx.EXPAND)
        self.rounds_slider.Bind(wx.EVT_SCROLL, self.Update())

        self.box_text = wx.StaticText(self, label="Choose difficulty")
        sizer_vertical.AddSpacer(40)
        sizer_vertical.Add(self.box_text, 0, wx.CENTER, 0)

        self.level_box = wx.ComboBox(
            self,
            choices=("Medium", "High"),
            style=wx.CB_READONLY
        )
        self.level_box.SetValue(specs["Value"][0])
        sizer_vertical.AddSpacer(10)
        sizer_vertical.Add(self.level_box, 0, wx.CENTER, 0)

        self.path_text = wx.StaticText(self, label="Storage directory")
        sizer_vertical.AddSpacer(30)
        sizer_vertical.Add(self.path_text, 0, wx.CENTER, 0)

        self.path = wx.StaticText(
            self,
            size=(wx.Size.GetWidth(self.Size), 20),
            style=wx.ALIGN_CENTER_HORIZONTAL
        )
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