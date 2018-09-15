import wx
from .view import View

class App(wx.App):

    def OnInit(self):
        View.init()
        return True
