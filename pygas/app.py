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
        #Player.init()
        # self.view = None
        # self.player = Player(self)
        Player.init()
        Artists.load()
        # self.albums = Albums(self)

        self.key_map = {
            'Left': lambda: self.view.switch_to('player'),
            'Right': self.switch_to_artists,
            'Up': lambda: self.view.scroll('Up'),
            'Down': lambda: self.view.scroll('Down'),
            'F1': self.reload_artists
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

    def switch_to_artists(self):
        self.view.switch_to('arts')
        self.show_artists()






    def play_album(self, alb_num, track_num):
        self.view.change_colors('albs', self.alb.num, alb_num)
        self.alb.num = alb_num
        self.view.set_font('rec', util.font_size(len(self.art.played + self.alb.played), 'info'));
        self.view.write_label('art', self.art.played)
        self.alb.played = self.albs[self.alb.num]
        self.view.write_label('alb', util.base(self.alb.played))
        self.view.write_label("sel_art", "")
        self.player.load_album(self.art.dirs[self.art.played], self.alb.played)
        tracks = self.get_tracks






