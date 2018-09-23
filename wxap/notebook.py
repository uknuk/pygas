import wx
from dotmap import DotMap
from .panel import Panel

class Notebook(wx.Notebook):

    def __init__(self, parent, keyhandler):
        wx.Notebook.__init__(self, parent)
        self.parent = parent
        self.handle_key = keyhandler

        self.pages = DotMap({
            "player": wx.Panel(self),
            "arts": wx.Panel(self)
        })

        self.panes = DotMap({
            "sel_arts": Panel(self.pages.arts),
            "albs": Panel(self.pages.player)
        })

        for title,page in self.pages.iteritems():
            #page.Bind(wx.EVT_KEY_DOWN, cls.on_key_down)
            self.AddPage(page, title.upper())

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panes.sel_arts, 1, wx.EXPAND)
        self.pages.arts.SetSizer(sizer)
