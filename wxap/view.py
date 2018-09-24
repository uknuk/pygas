import wx
#from dotmap import DotMap
from .panel import Panel


class View:

    @classmethod
    def init(cls, keyhandler):
        cls.win = wx.Frame(None, title="WXpython Audio Player", size=(cls.WIDTH, cls.HEIGHT))
        cls.win.Centre()


        cls.panel = Panel(cls.win, keyhandler)


        #cls.notebook = Notebook(cls.panel, keyhandler)
        #cls.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, cls.OnPageChanged)

        #cls.panel.Bind(wx.EVT_KEY_DOWN, cls.on_key_down)

        # cls.pages = DotMap({
        #     "player": wx.Panel(cls.notebook),
        #     "arts": wx.Panel(cls.notebook)
        #     })

        # for title,page in cls.pages.iteritems():
        #     #page.Bind(wx.EVT_KEY_DOWN, cls.on_key_down)
        #     cls.notebook.AddPage(page, title.upper())



        cls.win.Layout()



    @classmethod
    def add_buttons(cls, kind, labels, fun):
        #self.notebook.add_buttons(kind, labels, fun, cls.COLOR[kind], cls.FONT_SIZE[kind])
        cls.panel.add_buttons(kind, labels, fun, cls.COLOR[kind], cls.FONT_SIZE[kind])
        #cls.win.Show(True)

    @classmethod
    def on_key_down(cls, event):
        print event
        keycode = event.GetKeyCode()
        print keycode
        event.Skip()

    @classmethod
    def OnPageChanged(cls, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = cls.notebook.GetSelection()
        print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
        #cls.tabs[sel].SetFocus()
        event.Skip()
