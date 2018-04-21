#! /usr/bin/env python3
import gi
from gi.repository import GLib
from pygas import App

if __name__ == '__main__':
    GLib.set_prgname('Pygas')
    App().run()
