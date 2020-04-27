import wx
import wx.grid as gridlib

########################################################################
class PanelOne(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        grid = gridlib.Grid(self)
        grid.CreateGrid(25,12)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.EXPAND)
        self.SetSizer(sizer)

########################################################################
class PanelTwo(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.count = 0
        self.lbl = wx.StaticText(self,
                                 label='Counter: {}'.format(self.count))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

    #----------------------------------------------------------------------
    def start_timer(self):
        self.timer.Start(1000)

    #----------------------------------------------------------------------
    def stop_timer(self):
        self.timer.Stop()

    #----------------------------------------------------------------------
    def update(self, event):
        self.count += 1
        self.lbl.SetLabel('Counter: {}'.format(self.count))

########################################################################
class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Panel Switcher Tutorial")

        self.panel_one = PanelOne(self)
        self.panel_two = PanelTwo(self)
        self.panel_two.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)


        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_panels_menu_item = fileMenu.Append(wx.ID_ANY,
                                                  "Switch Panels",
                                                  "Some text")
        self.Bind(wx.EVT_MENU, self.onSwitchPanels,
                  switch_panels_menu_item)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

    #----------------------------------------------------------------------
    def onSwitchPanels(self, event):
        """"""
        if self.panel_one.IsShown():
            self.SetTitle("Panel Two Showing")
            self.panel_one.Hide()
            self.panel_two.Show()
            self.panel_two.start_timer()
        else:
            self.SetTitle("Panel One Showing")
            self.panel_one.Show()
            self.panel_two.stop_timer()
            self.panel_two.Hide()
        self.Layout()


# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()