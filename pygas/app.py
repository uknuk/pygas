import gi
from gi.repository import Gtk
from gi.repository import Gdk
from . import util
from .view import View
from .artists import Artists
from .albums import Albums
from .player import Player


class App(Gtk.Application):

    def __init__(self):
        super().__init__()
        Player.init()
        Artists.load()

        self.key_map = {
            'Left': lambda: View.switch_to('player'),
            'Right': App.switch_to_artists,
            'Up': lambda: View.scroll('Up'),
            'Down': lambda: View.scroll('Down'),
            'F1': Artists.reload,
            'space': Player.change_state
        }

    def do_startup(self):
        Gtk.Application.do_startup(self)
        View.init(self)
        View.win.connect('key_press_event', self.on_key_press)
        View.search.entry.connect(
            "search-changed", lambda w: Artists.show(View.search.entry.get_text()))

    @staticmethod
    def do_activate():
        Artists.show()
        Gtk.timeout_add(60*1000, lambda: Player.update_position())

    @staticmethod
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
    def switch_to_artists():
        View.switch_to('arts')
        Artists.show()








