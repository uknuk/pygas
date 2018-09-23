#! /usr/bin/env python3
import gi
from gi.repository import GLib
from pygas import App

GLib.set_prgname('Pygas')
App().run()
