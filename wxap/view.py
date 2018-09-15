import wx

class View:

    @classmethod
    def init(cls):
        cls.win = wx.Frame(None, title="WXpython Audio Player", size=(cls.WIDTH, cls.HEIGHT))
        cls.win.Centre()
        cls.win.Show(True)
