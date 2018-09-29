import gi

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

from .view import View
from .player import Player
from .artists import Artists
from .tracks import Tracks
from .albums import Albums
from .panel import Panel
from . import util

class App(Gtk.Application):

    def __init__(self):
        super().__init__()
        Player.init()

        self.key_map = {
            'Left': lambda: View.switch_to('player'),
            'Right': App.show_artists,
            'Up': lambda: View.scroll('Up'),
            'Down': lambda: View.scroll('Down'),
            'F1': Artists.reload,
            'F5': lambda: self.change_font(-1),
            'F6': lambda: self.change_font(1),
            'F11': lambda: Player.volume(-1),
            'F12': lambda: Player.volume(1),
            'space': Player.change_state,
            'Escape': Artists.restore
        }

    @classmethod
    def show_artists(cls):
        View.switch_to('arts')
        Artists.show()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        View.init(self)
        Artists.load()
        View.win.connect('key_press_event', self.on_key_press)
        View.search.entry.connect(
            "search-changed", lambda w: Artists.show(View.search.entry.get_text()))

    def do_activate(self):
        #Artists.show()
        try:
            with util.open_file(Tracks.LAST_FILE) as f:
                art, alb, num = [l.rstrip() for l in f.readlines()[:3]]
        except FileNotFoundError:
            num = None

        GLib.timeout_add(1000, lambda: Player.update_position())

        if num is not None:
            Artists.play(art, alb, num)

    def on_destroy(self):
        Player.stop()
        Gtk.main_quit()

    def on_key_press(self, _, event):
        key = Gdk.keyval_name(event.get_keyval()[1])
        if key in self.key_map:
            self.key_map[key]()
            return True
        else:
            return False

    @staticmethod
    def change_font(delta):
        Panel.font_size.tracks += delta
        Panel.font_size.albs += delta
        #print(View.font_size.tracks, View.font_size.albs)
        View.add_buttons('albs', Albums.shown, Albums.clicked, Albums.num)
        View.add_buttons('tracks', Tracks.shown, Tracks.clicked, Tracks.num)
