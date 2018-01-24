import os
from os import path
from .util import util
from .app import App
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
        with open(path.join(os.environ['HOME'], cls.DIRS_FILE)) as f:
            roots = f.readlines().pop().split()
            for r in roots:
                cls.names = os.listdir(r)
                for name in cls.names:
                    cls.dirs[name] = path.join(r, name)
                    cls.shorts[name] = util.cut(name, App.NAME_MAX['art'])

    @classmethod
    def reload(cls):
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
                Albums.show(names[0])
                return

            cls.shown = names
            View.set_font('sel_arts', util.font_size(list.reduce(names, lambda s, n: s + len(n), 0), 'items'))
            View.add_buttons('sel_arts', names, lambda n: cls.select(n))
        else:
            cls.view.clear('sel_arts')

        text = '' if entry is None else '" | "'.join([cls.shorts[n] for n in cls.names])
        View.buffer.set_text(text, -1)
        cls.view.win.show_all()

    @classmethod
    def select(cls, num):
        cls.chosen = cls.shown[num]
        if cls.chosen != cls.played:
            cls.view.write_label("sel_art", cls.chosen + ":")

        cls.app.albums.show(cls.dirs[cls.chosen])

    @classmethod
    def selected(cls):
        cls.played = cls.chosen

    @classmethod
    def played_directory(cls):
        return cls.dirs[cls.played]



