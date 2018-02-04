import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

from .view import View
from .player import Player
from .artists import Artists
from . import util


class App(Gtk.Application):

    def __init__(self):
        super().__init__()
        Player.init()
        Artists.load()

        self.key_map = {
            'Left': lambda: View.switch_to('player'),
            'Right': Artists.show,
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

    def do_activate(self):
        from . import LAST_FILE

        Artists.show()
        with util.open_file(LAST_FILE) as f:
            art, alb, num, _ = [l.rstrip() for l in f.readlines()]

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










