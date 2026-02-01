import os
import subprocess
import sys

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

from .container import Components
from .view import View
from .panel import Panel
from . import util


class App(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.tracks = Components.tracks()
        self.player = Components.player()
        self.artists = Components.artists()

        self.key_map = {
            'Left': lambda: View.switch_to('player'),
            'Right': self.show_artists,
            'Up': lambda: View.scroll('Up'),
            'Down': lambda: View.scroll('Down'),
            'F1': self.restart_app,
            'F5': lambda: self.change_font(-1),
            'F6': lambda: self.change_font(1),
            'space': self.player.change_state,
            'Escape': self.artists.restore
        }


    def restart_app(self, widget=None):
        print("Restarting application...")
        GLib.timeout_add(100, self.restart)

    def restart(self):
        class_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(class_dir)
        script = os.path.join(parent_dir, 'run.py')
        subprocess.Popen([sys.executable, script], cwd=parent_dir)

        self.quit()
        return False


    def show_artists(self):
        View.switch_to('arts')
        self.artists.show()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        View.init(self)
        self.artists.load()
        View.win.connect('key_press_event', self.on_key_press)
        View.search.entry.connect(
            "search-changed", lambda w: self.artists.show(View.search.entry.get_text()))

    def do_activate(self):
        try:
            with util.open_file(self.tracks.LAST_FILE) as f:
                art, alb, num = [line.rstrip() for line in f.readlines()[:3]]
        except FileNotFoundError:
            num = None

        GLib.timeout_add(1000, lambda: self.player.update_position())

        if num is not None:
            self.artists.play(art, alb, num)

    def on_destroy(self):
        self.player.stop()
        Gtk.main_quit()

    def on_key_press(self, _, event):
        key = Gdk.keyval_name(event.get_keyval()[1])
        if key in self.key_map:
            self.key_map[key]()
            return True
        else:
            return False

    def change_font(self, delta):
        Panel.font_size.tracks += delta
        Panel.font_size.albs += delta
        View.add_buttons('albs', self.albums.shown,
                         self.albums.clicked, self.albums.num)
        View.add_buttons('tracks', self.tracks.shown,
                         self.tracks.clicked, self.tracks.num)
