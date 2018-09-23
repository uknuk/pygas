import wx
import wx.lib.scrolledpanel as scrolled

class Panel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, style=wx.VSCROLL)
        self.SetupScrolling(scroll_x = False)
        self.parent = parent
        self.sizer = wx.WrapSizer()
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.SetFocus()


    def add_buttons(self, names, fun, color, fsize):
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
            self.sizer.Add(btn, 1, wx.EXPAND)
        print i


    def onSize(self, evt):
        size = self.GetSize()
        vsize = self.GetVirtualSize()
        self.SetVirtualSize((size[0], vsize[1]))
        evt.Skip()

    def on_key_down(self, event):
        print event.GetKeyCode()
        self.parent.GetParent().handle_key(event.GetKeyCode())
        event.Skip()
