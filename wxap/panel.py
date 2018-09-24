import wx
import wx.lib.scrolledpanel as scrolled
from dotmap import DotMap

class Panel(scrolled.ScrolledPanel):
    def __init__(self, parent, keyhandler):
        scrolled.ScrolledPanel.__init__(self, parent, style=wx.VSCROLL)
        self.SetupScrolling(scroll_x = False)
        self.parent = parent
        self.handle_key = keyhandler

        self.notebook = wx.Notebook(self)

        self.pages = DotMap({
            "player": wx.Panel(self.notebook),
            "arts": wx.Panel(self.notebook)
        })

        self.panes = DotMap({
            "sel_arts": wx.WrapSizer(),
            "albs": wx.BoxSizer(wx.VERTICAL)
        })

        for title,page in self.pages.iteritems():
            self.notebook.AddPage(page, title.upper())

        self.pages.player.SetSizer(self.panes.albs)
        self.pages.arts.SetSizer(self.panes.sel_arts)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 1)
        #self.sizer = wx.WrapSizer()
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.notebook.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.SetFocus()


    def add_pane_buttons(self, pane, names, fun, color, fsize):
        #print names
        font = wx.Font(fsize, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.SetFont(font)
        i = 0
        for name in names:
            txt = ' {} '.format(name)
            size = self.GetTextExtent(txt)
            #print name, size
            btn = wx.Button(self, i, txt, size=wx.Size(size[0] + 10, size[1] + 10))
            i += 1
            btn.SetForegroundColour(wx.BLUE)
            btn.Bind(wx.EVT_BUTTON, fun)
            pane.Add(btn, 1, wx.EXPAND)
        print i

    def add_buttons(self, kind, names, fun, color, fsize):
        self.add_pane_buttons(self.panes[kind], names, fun, color, fsize)



    def onSize(self, evt):
        size = self.GetSize()
        vsize = self.GetVirtualSize()
        self.SetVirtualSize((size[0], vsize[1]))
        evt.Skip()

    def on_key_down(self, event):
        print event.GetKeyCode()
        self.handle_key(event.GetKeyCode())
        event.Skip()
