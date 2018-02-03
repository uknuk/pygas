import os
from os import path
from . import util
from .view import View


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
        from .albums import Albums

        names = cls.names

        if entry:
            sel = entry[0:-1] if entry[-1] == '§' else entry
            names = list(filter(lambda a: a.replace('_', ' ').lower().startswith(sel), names))

            if len(names) == 1:
                Albums.show(cls.dirs[names[0]])
                return

            cls.shown = names
            View.font_size.arts = util.font_size(list.reduce(names, lambda s, n: s + len(n), 0), 'items')
            View.add_buttons('arts', names, lambda n: cls.select(n))
        else:
            View.clear('arts')

        text = '' if entry else '" | "'.join([cls.shorts[n] for n in names])
        View.switch_to('arts')
        View.buffer.set_text(text, -1)
        View.win.show_all()

    @classmethod
    def select(cls, num):
        from .albums import Albums

        cls.chosen = cls.shown[num]
        if cls.chosen != cls.played:
            cls.view.write_label("sel_art", cls.chosen + ":")

        Albums.show(cls.dirs[cls.chosen])

    @classmethod
    def play(cls, art, alb, t_num):
        from .albums import Albums

        cls.chosen = art
        Albums.show(cls.dirs[art])
        Albums.play_name(alb, t_num)

    @classmethod
    def selected(cls):
        cls.played = cls.chosen

    @classmethod
    def played_directory(cls):
        return cls.dirs[cls.played]



