import os
# from os import environ, path
from . import util
from .view import View


class Artists:
    def __init__(self, albums, tracks):
        self.albums = albums
        self.tracks = tracks
        self.names = []
        self.dirs = {}
        self.shorts = {}
        self.shown = []
        self.played = None
        self.chosen = None

    def load(self):
        self.tracks.inject(self, self.albums.next)
        self.albums.show_tracks = self.tracks.show

        try:
            with util.open_file(self.DIRS_FILE) as f:
                roots = f.readlines()[0].split()
        except FileNotFoundError:
            roots = [os.path.join(os.environ['HOME'], "Music")]
        
        for r in roots:
                names = os.listdir(r)
                self.names += names
                for name in names:
                    self.dirs[name] = os.path.join(r, name)
                    self.shorts[name] = util.cut(name, View.NAME_MAX['art'])

        self.names = sorted(self.names)
        self.shown = self.names
        View.panel.add_buttons('arts', [self.shorts[n] for n in self.names], self.clicked)

    def reload(self):
        self.names = []
        self.load()
        if View.stack.visible_child_name == "arts":
            self.show()

    def show(self, entry=None):
        names = self.names

        if entry:
            sel = entry[0:-1] if entry[-1] == '§' else entry
            names = list(filter(lambda a: a.replace('_', ' ').lower().startswith(sel), names))

            if len(names) == 1:
                self.select(names[0])
                self.albums.show(self.dirs[names[0]], self.tracks.shown)
                return

            self.shown = names
            View.panel.add_buttons('sel_arts', names, self.clicked)
        else:
            self.shown = names
            View.panel.clear('sel_arts')

        View.win.show_all()

    def clicked(self, _, num):
        self.select(self.shown[num])

    def select(self, name):
        self.chosen = name
        if self.chosen != self.played:
            View.panel.write_label("sel_art", self.chosen + ":")

        View.scroll("Up")
        self.albums.show(self.dirs[self.chosen], self.tracks.shown)

    def play(self, art, alb, t_num):
        self.chosen = art
        art_dir = self.dirs[art]
        self.albums.show(art_dir, self.tracks.shown)
        self.albums.play_name(os.path.join(art_dir, alb), int(t_num))

    def restore(self):
        View.panel.write_label("sel_art", '')
        self.chosen = self.played
        self.albums.show(self.dirs[self.chosen], self.tracks.shown, False)

    def selected(self):
        self.played = self.chosen

    def played_directory(self):
        return self.dirs[self.played]

    def get_played(self):
        return self.played, self.albums.played
