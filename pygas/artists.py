import os
from os import path
from functools import reduce
from . import util
from .view import View
from .albums import Albums
from .tracks import Tracks


class Artists:

    names = []
    dirs = {}
    shorts = {}
    shown = []
    played = None
    chosen = None

    @classmethod
    def load(cls):
        Tracks.inject(cls, Albums.next)
        Albums.show_tracks = Tracks.show

        with util.open_file(cls.DIRS_FILE) as f:
            roots = f.readlines()[0].split()
            for r in roots:
                names = os.listdir(r)
                cls.names += names
                for name in names:
                    cls.dirs[name] = path.join(r, name)
                    cls.shorts[name] = util.cut(name, View.NAME_MAX['art'])

        cls.names = sorted(cls.names)

    @classmethod
    def reload(cls):
        cls.names = []
        cls.load()
        if View.stack.visible_child_name == "arts":
            cls.show()

    @classmethod
    def show(cls, entry=None):
        names = cls.names

        if entry:
            sel = entry[0:-1] if entry[-1] == '§' else entry
            names = list(filter(lambda a: a.replace('_', ' ').lower().startswith(sel), names))

            if len(names) == 1:
                cls.select(names[0])
                Albums.show(cls.dirs[names[0]], Tracks.shown)
                return

            cls.shown = names
            View.set_items_font('sel_arts', names)
            View.add_buttons('sel_arts', names, cls.clicked)
        else:
            View.clear('sel_arts')

        text = '' if entry else " | ".join([cls.shorts[n] for n in names])
        View.buffer.set_text(text, -1)
        View.win.show_all()

    @classmethod
    def clicked(cls, _, num):
        cls.select(cls.shown[num])

    @classmethod
    def select(cls, name):
        cls.chosen = name
        if cls.chosen != cls.played:
            View.write_label("sel_art", cls.chosen + ":")

        Albums.show(cls.dirs[cls.chosen], Tracks.shown)

    @classmethod
    def play(cls, art, alb, t_num):
        cls.chosen = art
        art_dir = cls.dirs[art]
        Albums.show(art_dir, Tracks.shown)
        Albums.play_name(path.join(art_dir, alb), int(t_num))

    @classmethod
    def restore(cls):
        View.write_label("sel_art", '')
        cls.chosen = cls.played
        Albums.show(cls.dirs[cls.chosen], Tracks.shown, False)

    @classmethod
    def selected(cls):
        cls.played = cls.chosen

    @classmethod
    def played_directory(cls):
        return cls.dirs[cls.played]

    @classmethod
    def get_played(cls):
        return cls.played, Albums.played
