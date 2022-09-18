#! /usr/bin/env python3
import gi
import signal
from gi.repository import GLib
from pygas import App

GLib.set_prgname('Pygas')
app = App()
GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, app.quit)
app.run()
