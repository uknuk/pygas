import wx
from .view import View
from .artists import Artists

class App(wx.App):

    def OnInit(self):
        self.keymap = {
            wx.WXK_F1: lambda: View.panel.notebook.SetSelection(0),
            wx.WXK_F2: lambda: App.show_artists()
        }

        View.init(self.keyhandler)
        #View.win.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        Artists.load()
        # Artists.show()
        View.win.Show(True)
        return True

    @classmethod
    def show_artists(cls):
        Artists.show()
        View.panel.notebook.SetSelection(1)
        View.win.Show(True)

    def keyhandler(self, key):
        if key in self.keymap:
            self.keymap[key]()
