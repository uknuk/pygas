import wx
from dotmap import DotMap
from .panel import Panel

class View:

    @classmethod
    def init(cls):
        cls.win = wx.Frame(None, title="WXpython Audio Player", size=(cls.WIDTH, cls.HEIGHT))
        cls.win.Centre()
        cls.panes = DotMap({
            "sel_arts": Panel(cls.win)
            })
        #cls.win.Show(True)

    @classmethod
    def add_buttons(cls, kind, labels, fun):
        cls.panes[kind].add_buttons(labels, fun, cls.COLOR[kind], cls.FONT_SIZE[kind])
        cls.win.Show(True)
