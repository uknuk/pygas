import os
from os import path
from .util import util


class Artists:

    def __init__(self, app):
        self.app = app
        self.view = app.view
        self.dirs = {}

        self.names = []
        self.short = {}
        self.shown = []

        self.played = None
        self.chosen = None

        self.load()

    def load(self):
        with open(path.join(os.environ['HOME'], self.DIRS_FILE)) as f:
            roots = f.readlines().pop().split()
            for r in roots:
                self.names = os.listdir(r)
                for name in self.names:
                    self.dirs[name] = path.join(r, name)
                    self.short[name] = util.cut(name, self.app.NAME_MAX['art'])

    def reload(self):
        self.load()
        if self.view.stack.visible_child_name == "arts":
            self.show()

    def show(self, entry=None):
        names = self.names

        if entry:
            sel = entry[0:-1] if entry[-1] == '§' else entry
            names = list(filter(lambda a: a.replace('_', ' ').lower().startswith(sel), names))

            if len(names) == 1:
                self.app.show_albums(names[0])
                return

            self.shown = names
            self.view.set_font('sel_arts', util.font_size(list.reduce(names, lambda s, n: s + len(n), 0), 'items'))
            self.view.add_buttons('sel_arts', names, lambda n: self.select(n))
        else:
            self.view.clear('sel_arts')

        text = '' if entry is None else '" | "'.join([self.short[n] for n in self.names])
        self.view.buffer.set_text(text, -1)
        self.view.win.show_all()

    def select(self, num):
        self.chosen = self.shown[num]
        if self.chosen != self.played:
            self.view.write_label("sel_art", self.chosen + ":")

        self.app.albums.show(self.dirs[self.chosen])

    def selected(self):
        self.played = self.chosen



