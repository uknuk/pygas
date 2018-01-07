import gi
from gi.repository import Gtk
from . import util
from .view import View


class App(Gtk.Aplication):

    def __init__(self):
        super().__init__()
        self.player = None
        self.view = None
        self.art_dirs, self.art_names = util.load_artists()

    def run(self, player):
        self.player = player

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.view = View(self)

    def do_activate(self):
        self.show_artist()

    def show_artists(self):
        # arts = self.art_names.keys()
        # add entry
        text = self.art_dirs.values().join(" | ")
        return text
