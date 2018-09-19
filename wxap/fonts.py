import wx
import time

family = wx.DEFAULT
style = wx.NORMAL
weight = wx.NORMAL

test = "Ww"

app = wx.App()  # doesn't work without app
dc = wx.ScreenDC()

for size in range(10,33):
    font = wx.Font(size, family, style, weight)
    dc.SetFont(font)
    w,h = dc.GetTextExtent(test)
    print '%d: (%d, %d),' % (size, w/2, h)
