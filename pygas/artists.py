import os
from os import path
from functools import reduce
from . import util
from .view import View
from .albums import Albums



class Artists:

    names = []
    dirs = {}
    shorts = {}
    shown = []
    played = None
    chosen = None

    @classmethod
    def load(cls):
        from . import NAME_MAX

        with util.open_file(cls.DIRS_FILE) as f:
            roots = f.readlines().pop().split()
            for r in roots:
                names = os.listdir(r)
                cls.names += names
                for name in names:
                    cls.dirs[name] = path.join(r, name)
                    cls.shorts[name] = util.cut(name, NAME_MAX['art'])

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
                Albums.show(cls.dirs[names[0]])
                return

            cls.shown = names
            View.font_size.sel_arts = util.font_size(reduce(lambda s, n: s + len(n), names, 0), 'items')
            View.add_buttons('sel_arts', names, cls.clicked)
        else:
            View.clear('sel_arts')

        text = '' if entry else " | ".join([cls.shorts[n] for n in names])
        View.switch_to('arts')
        View.buffer.set_text(text, -1)
        View.win.show_all()

    @classmethod
    def clicked(cls, _, num):
        cls.select(num)

    @classmethod
    def select(cls, num):
        cls.chosen = cls.shown[num]
        if cls.chosen != cls.played:
            View.write_label("sel_art", cls.chosen + ":")

        Albums.show(cls.dirs[cls.chosen])

    @classmethod
    def play(cls, art, alb, t_num):
        cls.chosen = art
        art_dir = cls.dirs[art]
        Albums.show(art_dir)
        Albums.play_name(path.join(art_dir, alb), int(t_num))

    @classmethod
    def selected(cls):
        cls.played = cls.chosen

    @classmethod
    def played_directory(cls):
        return cls.dirs[cls.played]



