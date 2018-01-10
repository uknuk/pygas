import gi
from gi.repository import Gtk
from gi.repository import Gdk
from . import util
from .view import View


class App(Gtk.Application):

    def __init__(self):
        super().__init__()
        self.player = None
        self.view = None
        self.art_dirs, self.art_names = util.load_artists(self.DIRS_FILE, self.NAME_MAX)

        self.key_map = {
            'Left': lambda: self.view.switch_to('player'),
            'Right': self.show_artists,
            'Up': lambda: self.view.scroll('Up'),
            'Down': lambda: self.view.scroll('Down'),
            'F1': self.reload_artists
        }

    def run(self, player):
        self.player = player
        super().run()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.view = View(self)
        self.view.win.connect('key_press_event', self.on_key_press)
        self.view.search.entry.connect(
            "search-changed", lambda w: self.show_artists(self.view.search.entry.get_text()))

    def do_activate(self):
        self.show_artists()
        self.player.init(self.view)

    def on_quit(self):
        self.quit()

    def on_key_press(self, widget, event):
        key = Gdk.keyval_name(event.get_keyval()[1])
        if key in self.key_map:
            self.key_map[key]()
            return True
        else:
            return False

    def show_artists(self, entry=None):
        self.view.switch_to('arts')
        arts = self.art_names.keys()
        if entry:
            arts = list(filter(lambda a: a.replace('_', ' ').lower().startswith(entry), arts))

        text = " | ".join([self.art_names[a] for a in arts])
        self.view.buffer.set_text(text, -1)
        self.view.win.show_all()

    def reload_artists(self):
        self.art_dirs, self.art_names = util.load_artists(self.DIRS_FILE, self.NAME_MAX)
        if self.view.stack.visible_child_name == "arts":
            self.show_artists()
