import os
from os import path
from functools import reduce
from . import util
from .view import View
#from .albums import Albums
#from .tracks import Tracks


class Artists:

    names = []
    dirs = {}
    shorts = {}
    shown = []
    played = None
    chosen = None

    @classmethod
    def load(cls):
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
    def show(cls, entry=None):
        names = cls.names
        View.add_buttons('sel_arts', [cls.shorts[n] for n in names], cls.clicked)

    @classmethod
    def clicked(cls, event):
        print event.GetId()
