import wx
from .view import View
from .artists import Artists

class App(wx.App):

    def OnInit(self):
        View.init()
        Artists.load()
        Artists.show()
        return True
